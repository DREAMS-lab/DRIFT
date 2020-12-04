# Standard Python Libraries
import logging
import os
import sys
import shutil
import time
from typing import Any, Dict

# Third-Party Libraries
import docker
from docker.types import Mount
from .logger import LOGGER, DEBUG, ERROR

# Constants
IMAGE_NAME = "pascal0x90/basic_phuzzer"
AFL_LOCATION = "/phuzzers/AFLplusplus"

class Container:
    """Class defines interface container for the user with DRIFT."""

    def __init__(self, git_repo: str = "", binary: str = "", dic: str = "", workdir: str = "", port: int = 8888):
        """Initialize the object with repo of choice and binary."""
        self.git = git_repo
        self.binary = binary
        self.dic = dic
        self.port = port
        self.workdir = workdir
        self.client = None
        self.fpid = -1  # IN docker pid
        self.container = None   # Container 

    def create_session(self):
        """Create the session, make sure we have all the args we need."""
        """
        Do this in steps:   
            1. Start up docker container (make sure stuff is installed)
                1.2. Startup with a mounted volume (empty folder)
            3. We clone repo into this directory
            4. Copy any config files we need into repo
        """
        # Local vars
        container = None

        # Check if there is already a docker container running
        client = docker.from_env()

        # Grab current images
        images = ', '.join([', '.join(i.tags) for i in client.images.list()])

        # Check if the image exists
        if IMAGE_NAME not in images:
            DEBUG.debug("Image does not exist")
            LOGGER.info("Pulling image")
            # Pull the image
            image = client.images.pull(IMAGE_NAME)

        #TODO: Maybe add in some checks for the user's convenience
        # of not running 500 containers without checking. 

        # Make sure we have a work directory
        DEBUG.debug("Checking if current work directory exists")
        if os.path.isdir(self.workdir) or os.path.isdir("workdir"):
            print("A work directory exists...Delete?")
            user_in = ""
            while user_in not in ['y', 'Y', 'n', 'N']:
                user_in = input()
            if user_in in ['y', 'Y']:
                DEBUG.debug("Removing previous work directory")
                try:
                    shutil.rmtree(self.workdir)
                except:
                    shutil.rmtree("workdir")
            else:
                DEBUG.debug("Backing up current work directory...")
                if self.workdir != "":
                    shutil.move(self.workdir, f"{self.workdir}_bak")
                else:
                    shutil.move(self.workdir, f"workdir_bak")
        # If we are not using a workdir (ie in the cli or ci) 
        # then dont create the build folder
        print(self.workdir)
        if self.workdir != "":
            LOGGER.info("Making build folder")
            os.mkdir(self.workdir)
            os.mkdir(f"{self.workdir}/build")
        else:
            LOGGER.info("Skipping build folder make")
            self.workdir = "workdir"
            os.mkdir("workdir")

        # Create volumes
        volume = {
            os.path.join(os.getcwd(), 'resources'): {
                'bind' : '/DRIFT', 
                'mode' : 'rw'
            },
            os.path.join(os.getcwd(), self.workdir): {
                'bind' : '/DRIFT/workdir',
                'mode' : 'rw'
            },
            "/home/ubuntu/.ssh": {
                'bind' : '/root/.ssh',
                'mode' : 'rw'
            }
        }

        # Set ports
        DEBUG.debug(f"Forwarding port {self.port}")
        port = {
            '8888/tcp':self.port
        }

        # Begin the container
        container = client.containers.run(
            IMAGE_NAME, 
            "tail -f /dev/null", 
            detach=True,
            privileged=True, 
            volumes=volume,
            remove=True,
            ports=port
        )
        DEBUG.debug(f"\tContainer Name: {container.name}\n\t\tID: {container.id}\n\t\tTag: {container.image.tags[0]}\n\t\tPorts: {container.ports}\n\t\tVolumes: {container.attrs['Config']['Volumes']}")

        # Assign attrributes to class
        self.container = container
        self.client = client

        LOGGER.info("Container initialized!")

    def setup_container(self):
        """This will setup the container."""
        # Setup our core dumps on the container
        DEBUG.debug("Adjusting cores and scheduling")
        self.container.exec_run("bash -c 'echo core > /proc/sys/kernel/core_pattern'", user='root', workdir="/DRIFT/")
        self.container.exec_run("bash -c 'echo 1 > /proc/sys/kernel/sched_child_runs_first'", user='root', workdir="/DRIFT/")
        # Fix python
        DEBUG.debug("Removing python2. Return to python3")
        self.container.exec_run("bash -c 'rm /usr/bin/python'", user='root')
        self.container.exec_run("bash -c 'ln -s /usr/bin/python3 /usr/bin/python'", user='root', workdir="/DRIFT/")
        

    def grab_project(self):
        """This will clone git project into work dir and prep for compliation."""
        """
        The project should contain the following:
            - setup.sh
            - project code
        setup.sh is responsible for compiling code
        """
        DEBUG.debug("Clone project repository (from git{hub/lab})")
        print(self.container.exec_run(f"bash -c 'git clone {self.git} /DRIFT/workdir/project'", user="root").output)
        LOGGER.info(f"Successfully logged {self.git}")
        
    def compile_project(self):
        """Compiles the project in the project folder titled "project". """
        """
        The project must make sure in the setup.sh file that:
            - output binary goes to "/DRIFT/workdir/build"
        If this is not the case, then "it should".
        """
        DEBUG.debug("Compiling project..")
        print(self.container.exec_run(f"bash -c './setup.sh {AFL_LOCATION} {self.binary}'", user="root", workdir="/DRIFT/workdir/project"))
        LOGGER.info(f"Successful compilation of {self.binary}. Located in /DRIFT/build (hopefully)")

    #TODO: Add ability to pass arguments to fuzzer (phuzzer has it, just need to implement)
    def begin_fuzzing(self, args: str =""):
        """Starts fuzzing the binary."""
        # python3 -m phuzzer -p AFL++ -c 1 -w /phuzzui/workdir "/phuzzui/build/$binary"
        LOGGER.info(f"Begin fuzzing on /DRIFT/build/{self.binary}")
        print(self.container.exec_run(f'python3 -m phuzzer -p AFL++ -c 2 -d 2 -w /DRIFT/workdir/phuzwork "/DRIFT/workdir/build/{self.binary}"', detach=True).output)
        # Wait for the dir to be created. Cant really do this better at the moment
        time.sleep(6)
        DEBUG.debug("Fixing perms so we can read directory.")
        self.container.exec_run(f"chmod +rwx -R /DRIFT/workdir/phuzwork", user="root")

    def web(self, port: int, path: str):
        """This is the main interface with the container to start a web server."""
        self.container.exec_run(f'bash -c "cd {path}; ./start.sh"', user="root", detach=True)
        DEBUG.debug(f"Web server started on port {port}")

    def kill(self):
        """This will close out the container and the processes."""
        # Kill phuzzer
        self.container.exec_run('bash -c "ps -ef | grep tail | grep -v grep | awk \'{print $2}\' | xargs -r kill -9"', user='root').output
        DEBUG.debug("Phuzzing process killed")

        # Kill container
        self.container.kill()
        
        LOGGER.info("Container killed")

# ps -ef | grep tail | grep -v grep | awk '{print $2}' | xargs -r kill -9
