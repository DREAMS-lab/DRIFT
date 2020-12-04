"""DRIFT is a drone research fuzzing tool

Drone Research Integrated Development Tool (DRIFT) is designed to
aid in the development of drone software and firmware. The program
aims to help developers find and create new and unique test cases
which can increase the reliability and robustness of the software
they create. THIS APP WILL ELEVATE ITS PRIVILEGES TO ROOT.

EXIT STATUS
    This utility exits with one of the following values:
    0   Execution completed successfully.
    >0  An error occurred.

Usage:
  drift overwatch <regressionRepo>
  drift cli <binary> <gitRepo> [--dictionary=DICT] [--args=ARGS] [--workdir=DIR] [--web] [--port=PORT]
  drift web [-p | --port=PORT]
  drift (-h | --help)

Options:
  -h --help                 Show this message.
  --version                 Show the current version
  --web                     Open a web server on PORT which shows
                            the current progress of the CLI.
  --port=PORT               Define port number to host/attach.
                            to the WebGUI on. [default: 8888]
  --dictionary=DICT         Define a path to a dictionary you
                            wish to use in the fuzzing proccess.
  --args=ARGS               Define arguments to be sent to the
                            target being fuzzed. [default: @@]
  --workdir=DIR             Define where the work directory
                            should be. [default: workdir]
"""

# Standard Python Libraries
import logging
import os
import sys
from typing import Any, Dict

# Third-Party Libraries
import docopt
from elevate import elevate
import pkg_resources
from schema import And, Or, Schema, SchemaError, Use

from ._version import __version__

# Local Imports
from .cli import CLI
from .logger import DEBUG, ERROR, LOGGER
from .overwatch import Overwatch
from .web import WEB


def drift_web(port: int = 8888) -> int:
    """Trigger the DRIFT WebUI to start."""
    print("Current port", port)
    # Create the web object which creates container
    w = WEB(port)

    # Start the web server
    print("Starting web server on ", port)
    w.begin_web()

    return 0


def drift_cli(
    git_repo: str, binary: str, dic: str, workdir: str, cliweb: bool, port: int
) -> int:
    """Trigger the DRIFT CLI to start."""
    # Create CLI object
    c = CLI(git_repo, binary, dic, workdir, port)

    # Setup container for fuzzing a project
    c.setup_fuzzing()

    # Start the fuzzing
    c.start()

    # Decide how to monitor progress
    if cliweb:
        c.begin_web(port)
    else:
        c.stats_master()
    return 0


def drift_overwatch(reg_repo: str) -> int:
    """Trigger the DRIFT Overwatch tool."""
    # Create overwatch object
    print("create object")
    o = Overwatch(reg_repo, workdir="workdir")

    # Create the regression testing repo folder
    print("create")
    o.reg_repo()

    # Setup observer and tracer
    """
    This is a multithreaded ordeal. The idea is:
        - observer: Looks for crashes in {/DRIFT/workdir}
        - tracer:   Will start a fuzzer for the binary in project

    *Ideally we want to be able to host multiple projects at once
    but realistically that may not be the most stable right now.
    """
    o.watch_n_launch()
    return 0


def main() -> int:
    """Parse arguments and call function based on what was passed"""
    args: Dict[str, str] = docopt.docopt(__doc__, version=__version__)
    # Validate and convert arguments as needed
    schema: Schema = Schema(
        {
            "<binary>": Or(
                None,
                And(
                    str,
                    Use(str.lower),
                ),
            ),
            "<gitRepo>": Or(
                None,
                Use(str),
            ),
            "<regressionRepo>": Or(
                None,
                Use(str),
            ),
            "--port": Or(
                None,
                Use(int),
            ),
            "--dictionary": Or(
                None,
                Use(str),
            ),
            "--workdir": Or(
                None,
                Use(str),
            ),
            str: object,  # Don't care about other keys, if any
        }
    )

    try:
        validated_args: Dict[str, Any] = schema.validate(args)
    except SchemaError as err:
        # Exit because one or more of the arguments were invalid
        print(err, file=sys.stderr)
        return 1

    # Assign validated arguments to variables
    binary: str = validated_args["<binary>"]
    git_repo: str = validated_args["<gitRepo>"]
    reg_repo: str = validated_args["<regressionRepo>"]
    port: int = validated_args["--port"]
    dic: str = validated_args["--dictionary"]
    workdir: str = validated_args["--workdir"]
    if workdir == None or workdir == "":
        workdir = "workdir"

    # Boolean deciders
    overwatch: bool = validated_args["overwatch"]
    cli: bool = validated_args["cli"]
    web: bool = validated_args["web"]
    cliweb: bool = validated_args["--web"]

    # Make sure the user is root
    cwd = os.getcwd()  # Save current working dir
    elevate(graphical=False)
    os.chdir(cwd)  # Take it back now yall\
    sys.path.append(cwd)

    # Call respective function based on call
    if overwatch:
        drift_overwatch(reg_repo)
    elif cli:
        # TODO: Add argument support for cli
        drift_cli(git_repo, binary, dic, workdir, cliweb, port)
    elif web:
        drift_web(port)

    return 0


if __name__ == "__main__":
    sys.exit(main())
