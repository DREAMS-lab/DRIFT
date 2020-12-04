# Standard libraries
import signal
import sys

# Local libraries
from . import container
from .logger import DEBUG, LOGGER


class WEB:
    """WEB interface for user and container which has been made."""

    def __init__(self, port: int = 8080):
        self.container = container.Container(port=port)
        self.container.create_session()
        self.container.setup_container()
        self.port = port

    def begin_web(self):
        """Begin the web ui to start fuzzing binaries."""
        LOGGER.info(f"Starting web UI on port {self.port}")
        signal.signal(signal.SIGINT, self.signal_handling)
        self.container.web(self.port, "/DRIFT/webUI")

        # Wait till the user wants to quit
        while True:
            try:
                pass
            except KeyboardInterrupt:
                DEBUG.debug("Cleaning up!")
                # Move work dir into our workdir
                self.container.container.exec_run(
                    f"bash -c 'cp -r /dev/shm/work/* /DRIFT/workdir/.'", user="root"
                )
                self.container.container.exec_run(
                    f"chmod +rwx -R /DRIFT/workdir/phuzwork", user="root"
                )

                # Kill `the container
                # self.container.kill()
                break  # Lets get out of here
        return 0

    def signal_handling(self, signum, frame):
        """
        Handle ctrl+c.
        """
        DEBUG.debug("Cleaning up!")

        # Kill container
        try:
            # Move work dir into our workdir
            self.container.container.exec_run(
                f"bash -c 'cp -r /dev/shm/work/* /DRIFT/workdir/.'", user="root"
            )
            self.container.container.exec_run(
                f"chmod +rwx -R /DRIFT/workdir/phuzwork", user="root"
            )
            self.container.kill()
        except:
            pass
        sys.exit(0)
