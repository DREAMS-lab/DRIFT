#!/usr/bin/env pythonn3

import sys
import os
import subprocess
import threading
import time
import signal
from log import *

# globals
REGREPO = None
REGREPOS = "./regrepos"
CRASHPATH = "../arena/workdir/fuzzer-master/crashes/"

# Setup signaling
def signal_handling(signum, frame):
    '''Handle ctrl+c.'''
    LOGGER.info("Exiting cleanly...")

    # Exit irl
    sys.exit(0)

class Observer:
    '''Observer object will handle observations of directory.'''

    def __init__(self):
        '''Initialize the object.'''
        st = REGREPO.split("/")
        for i in st:
            if ".git" in i:
                self.repo = i.split(".")[0]
                LOGGER.info(f"Set repo to {self.repo}")
        self.crash = CRASHPATH
    def init(self):
        '''Check if the crash file exists. wait if not.''' 
        LOGGER.info("Wait for the 'crashes' directory to exist...")
        while not os.path.exists(CRASHPATH):
            pass
        DEBUG.debug("Crashes directory has been found. Continuing.")
    def observe(self):
        '''Begin observing the crash directory.'''
        seen = [] # This is the seen crash input files
        while True:
            # Check all current files in the directory
            files = os.listdir(CRASHPATH)
            try:
                files.remove("README.txt")
            except:
                pass
            
            # Iterate over files and move to reg tester
            for f in files:
                if f not in seen:
                    LOGGER.info("New crash found!")
                    seen.append(f)
                    DEBUG.debug("Copying to REGREPO dir.")
                    os.system(f"cp {CRASHPATH + f} {REGREPOS}/{self.repo}/.")
                    os.system(f"cd {REGREPOS}/{self.repo}; git add --all; git commit -m 'New crash {f}'; git push")



def check_root() -> int:
    '''Check if the effective user id is root.'''
    if os.geteuid() != 0:
        ERROR.error("Please run script with elevated permissions")
        print('''
        Why do I need elevated perms??
        - Access to crashes folder in workdir requires root
        - World domination
        ''')
        sys.exit(-1)
    else:
        return 0

def define_reg_repo():
    '''Set the global regression testing repository.'''
    global REGREPO
    if ".git" not in sys.argv[1]:
        ERROR.error("Must be a valid git url!")
    REGREPO = sys.argv[1]

def clone_repo():
    '''Clone the regtest repo.'''
    # Check if regrepos folder exists
    if not os.path.exists(REGREPOS):
        # Create the dir since it doesnt exist
        LOGGER.info("Path DNE, creating REREPOS dir.")
        os.mkdir(REGREPOS)
    # Clone reg repo into this
    LOGGER.info("Cloning regression testing repo into regrepos dir.")
    os.system(f"cd {REGREPOS}; git clone {REGREPO}")


# Make sure we are root
check_root()

# define and clone repo
define_reg_repo()
clone_repo()

# start signal handling
signal.signal(signal.SIGINT, signal_handling)

# Make our observer object
obs = Observer()
obs.init()

# Start observing
obs.observe()
