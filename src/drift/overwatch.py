# Standard Python Libraries
import base64
import logging
import os
import signal
import sys
import threading
import time
from typing import Any, Dict

# Third-Party Libraries
import docker

# Local libraries
from . import container
from .logger import DEBUG, ERROR, LOGGER


class phuzzer_start(threading.Thread):
    """
    This will begin the container fuzzer on the binary.
    """

    def __init__(self, container: container.Container, port: int = 8888):
        """Initialize the fuzzing handler."""
        # Create pipes
        self.port = port
        threading.Thread.__init__(self)
        self.container = container

    def run(self):
        """
        run will setup and begin fuzzing the binary
        """
        # self.container.begin_fuzzing("python3 -m phuzzer -p AFL++ -c 1 -w /phuzzui/workdir "/phuzzui/build/$binary"")
        print(self.container.begin_fuzzing())
        print("Fuzzing Started!")
        while True:
            pass

    # TODO: Implement for multiple fuzzing instances so we can see multiple progresses
    # def begin_web(self, port: int = 8888) -> int:
    #     """
    #     Begin the web server to monitor the cli.
    #     """
    #     self.container.web(port, "/DRIFT/cliUI")

    #     # Wait till the user wants to quit
    #     while True:
    #         try:
    #             pass
    #         except KeyboardInterrupt:
    #             print("Cleaning up!")
    #             # Kill `the container
    #             self.container.kill()
    #             break # Lets get out of here
    #     return 0


class LaunchObserver(threading.Thread):
    """
    This handles the launching of observer
    """

    def __init__(
        self, container: docker.models.containers.Container, repo: str, port: int = 8888
    ):
        """Initialize the fuzzing handler."""
        # Create pipes
        self.port = port
        threading.Thread.__init__(self)
        self.container = container
        self.repo = repo

    def run(self):
        """
        Observer will observe the crashes directory and copy new files into the reg repo.
        """
        # The files we have seen
        seen = []

        # Crash path
        CRASHDIR = "workdir/phuzwork/fuzzer-master/crashes/"
        REGREPOS = "workdir/regrepos/"

        # Wait for directory to exist
        while not os.path.exists(CRASHDIR):
            pass

        # Just keep watching the folder
        print("Starting observation")
        while True:
            # List out directory
            files = os.listdir(CRASHDIR)
            try:
                files.remove("README.txt")
            except:
                pass

            # Iterate over the files and move to regfolder
            for f in files:
                if f not in seen:
                    seen.append(f)
                    os.system(f"cp {CRASHDIR + f} {REGREPOS + self.repo}/.")
                    os.system(
                        f"cd {REGREPOS}/{self.repo}; git add --all; git commit -m 'New crash {f}'; git push"
                    )


class Overwatch:
    """Overwatch handles regression testing repo overhead for CI."""

    def __init__(self, git_repo: str, workdir: str = "workdir", port: int = 8888):
        """Initialize Overwatch obj."""
        # Initialize the container content
        self.container = container.Container(git_repo, port=port, workdir=workdir)
        # Start up the container
        self.container.create_session()
        # Setup for fuzzing environment
        self.container.setup_container()
        self.git = git_repo  # git repo used for regression testing
        self.repo = ""  # Project repo
        self.workdir = workdir
        self.port = port

    def reg_repo(self):
        """
        reg_repo sets up the regression testing repo dir.
        """
        # Parse out the repo
        st = self.git.split("/")
        for val in st:
            if ".git" in val:
                self.repo = val.split(".")[0]
                break

        # inside workdir, make regression testig folder
        # ssh-keyscan github.com >> ~/.ssh/known_hosts
        #print(self.container.container.exec_run("bash -c 'ssh-keygen -t rsa -f /root/.ssh/ida_rsa -q -N \"\"'", user="root"))
        LOGGER.info("YOU WILL NEED TO PUT A KEY THAT CAN PULL FROM GIT INTO YOUR .SSH FOLDER")
        os.system(f"git clone {self.git} workdir/regrepos/{self.repo}")
        self.container.container.exec_run(
            "bash -c 'printf \"Host github.com\n\tStrictHostKeyChecking no\n\" > ~/.ssh/config'", user="root"
        )
        self.container.container.exec_run(
            "bash -c 'ssh-keyscan github.com >> ~/.ssh/known_hosts'", user="root"
        )
        self.container.container.exec_run(
            "bash -c 'chmod 600 ~/.ssh/config'", user="root"
        )
        self.container.container.exec_run(
            "bash -c 'chown root ~/.ssh/config'", user="root"
        )
        self.container.container.exec_run(
            "bash -c 'chmod 600 ~/.ssh/id_rsa'", user="root"
        )
        self.container.container.exec_run(
            "bash -c 'chown root ~/.ssh/id_rsa'", user="root"
        )
        self.container.container.exec_run(
            "bash -c 'git config --global user.name \"Pascal-0x90\"'"
        )
        self.container.container.exec_run(
            "bash -c 'git config --global user.email nksmith6@asu.edu'"
        )
        #print(self.container.container.exec_run("cat /root/.ssh/id_rsa"))

    def watch_n_launch(self):
        """
        Launch off our observer and the tracer (hopefully)
        """
        """
        The idea is to multi thread this and make it into something
        that can handle multiple fuzzing instances. Unfortunately the
        resources we were given did not suffice this therefore we were
        unable to test the success of multithreaded mutli fuzzers.

        For this reason we have single threaded overwatch. The only multi
        threading comes from the observer for the repo. Godspeed.
        """
        signal.signal(signal.SIGINT, self.signal_handling)

        # +++ Tracer +++#
        # Wait for file to exist then do stuff
        while not os.path.exists("resources/launch"):
            pass

        # Parse out launch file
        dat = open("resources/launch", "r").read().split("#")

        # Hopefully its at least a length of 2
        assert len(dat) == 2

        # Grab params from input
        git = dat[0]
        binary = dat[1]

        # Log out
        LOGGER.info(f"Pulling from {git}")
        LOGGER.info(f"Compiling into {binary}")

        # Remove the launch file
        os.remove("resources/launch")

        # Modify our container object
        self.container.git = git
        self.container.binary = binary

        # Compile the code
        self.setup_fuzzing()

        # Start phuzzer_start
        phuzzer = phuzzer_start(self.container)
        lo = LaunchObserver(self.container, self.repo, self.port)
        phuzzer.start()

        # Start the observer
        lo.start()

        # Do web things
        self.begin_web()

        # Join threads
        phuzzer.join()
        lo.join()

    def setup_fuzzing(self):
        """This will setup project for fuzzing."""
        # Will throw project into workdir, project folder called 'project'
        self.container.grab_project()

        # Run the compiling script on the project
        self.container.compile_project()

    def begin_web(self, port: int = 8888) -> int:
        """Begin the web server to monitor the cli."""
        print("Starting web server on ", port)
        self.container.web(port, "/DRIFT/cliUI")

        # Wait till the user wants to quit
        while True:
            try:
                pass
            except KeyboardInterrupt:
                print("Cleaning up!")
                # Kill `the container
                self.container.kill()
                break  # Lets get out of here
        return 0

    # Setup signaling
    def signal_handling(self, signum, frame):
        """
        Handle ctrl+c.
        """
        print("Exiting cleanly...")

        self.container.kill()

        # Exit irl
        sys.exit(0)
