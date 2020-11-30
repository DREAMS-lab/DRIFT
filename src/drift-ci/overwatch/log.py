#!/usr/bin/env python3

# Import logging class
import logging

# Define custom logger class
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class Formatter(logging.Formatter):
    '''Logging formatter. Add colors and what not.'''
    
    green = "\033[1;32m"
    red = "\033[1;31m"
    white = "\033[1;37m"
    reset = "\033[0m"
    aformat = "%(levelname)s     | %(message)s\033[0m"

    FORMATS = {
        logging.DEBUG: white + aformat + reset,
        logging.INFO: green + aformat + reset,
        logging.WARNING: red + aformat + reset,
        logging.ERROR: red + aformat + reset,
        logging.CRITICAL: red + aformat + reset
    }

    def format(self,record):
        logfmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(logfmt)
        return formatter.format(record)

# Define constants
LOGLEVEL = logging.INFO
LOGGER = None
CHANNEL = None
ERROR = None
ECHAN = None
DEBUG = None
DCHAN = None

def init_logging():
    '''Setup logging for process.'''
    global LOGGER
    global CHANNEL
    global ERROR
    global ECHAN
    global DEBUG
    global DCHAN
    
    # Basic logging
    LOGGER = logging.getLogger('info')
    LOGGER.setLevel(LOGLEVEL)
    CHANNEL = logging.StreamHandler()
    CHANNEL.setLevel(LOGLEVEL)
    CHANNEL.setFormatter(Formatter())
    LOGGER.addHandler(CHANNEL)
    
    # Error logging
    ERROR = logging.getLogger('errors')
    ERROR.setLevel(logging.ERROR)
    ECHAN = logging.StreamHandler()
    ECHAN.setLevel(logging.ERROR)
    ECHAN.setFormatter(Formatter())
    ERROR.addHandler(ECHAN)

    # Debug logging
    DEBUG = logging.getLogger('DEBUG')
    DEBUG.setLevel(logging.DEBUG)
    DCHAN = logging.StreamHandler()
    DCHAN.setLevel(logging.DEBUG)
    DCHAN.setFormatter(Formatter())
    DEBUG.addHandler(DCHAN)

# Initialize logging 
init_logging()
