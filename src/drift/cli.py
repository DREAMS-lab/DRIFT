# Standard Python Libraries
import os
import time

# Local libraries
from . import container
from .logger import DEBUG


class CLI:
    """Cli interface for user and container which has been made."""

    def __init__(
        self,
        git_repo: str,
        binary: str,
        dic: str,
        workdir: str = "workdir",
        port: int = 8888,
    ):
        # Initialize the container content
        self.container = container.Container(git_repo, binary, dic, workdir, port)
        # Start up the container
        self.container.create_session()
        # Setup for fuzzing environment
        self.container.setup_container()
        self.git = git_repo
        self.binary = binary
        self.dict = dic
        self.workdir = workdir

    def setup_fuzzing(self):
        """This will setup project for fuzzing."""
        # Will throw project into workdir, project folder called 'project'
        print(self.container.grab_project())

        # Run the compiling script on the project
        print(self.container.compile_project())

    def start(self):
        """bEGIN THE FUZZING."""
        # Begin fuzzing??
        # self.container.begin_fuzzing("python3 -m phuzzer -p AFL++ -c 1 -w /phuzzui/workdir "/phuzzui/build/$binary"")
        print(self.container.begin_fuzzing())

    def begin_web(self, port: int = 8888) -> int:
        """Begin the web server to monitor the cli."""
        self.container.web(port, "/DRIFT/cliUI")

        # Wait till the user wants to quit
        while True:
            try:
                pass
            except KeyboardInterrupt:
                DEBUG.debug("Cleaning up!")
                # Kill `the container
                self.container.kill()
                break  # Lets get out of here
        return 0

    def stats_master(self) -> int:
        """This will read the content of the log file."""
        print(
            f"{os.path.join(os.getcwd(), self.workdir)}/phuzwork/fuzzer-master/fuzzer_stats"
        )

        # Make sure the work directory exists
        assert os.path.isdir(f"{self.workdir}/phuzwork/fuzzer-master")

        # While loop to keep running the stat check
        stats = {}

        while True:
            try:
                os.system("clear")
                # Open our stats file pointer
                stats_file = open(
                    f"{os.path.join(os.getcwd(), self.workdir)}/phuzwork/fuzzer-master/fuzzer_stats"
                )

                # Read in
                data = stats_file.read().split("\n")
                data = data[:-1]
                for value in data:
                    splitter = value.replace(" ", "").split(":")
                    stats[splitter[0]] = splitter[1]

                # Log out the information
                print(
                    f"Start time: {stats['start_time']}\nExecs/sec: {stats['execs_per_sec']}\nCrashes: {stats['unique_crashes']}"
                )

                time.sleep(2)

                # Reset to the beginning
                stats_file.close()
            except IndexError:
                pass
            except KeyboardInterrupt:
                print("Cleaning up!")
                # Kill `the container
                self.container.kill()

                # break from loop so we can return
                break
        return 0
