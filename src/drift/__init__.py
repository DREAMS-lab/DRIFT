"""The drift library."""
# We disable a Flake8 check for "Module imported but unused (F401)" here because
# although this import is not directly used, it populates the value
# package_name.__version__, which is used to get version information about this
# Python package.
from ._version import __version__  # noqa: F401
from .cli import CLI
from .container import IMAGE_NAME, Container
from .logger import (
    CHANNEL,
    DCHAN,
    DEBUG,
    ECHAN,
    ERROR,
    LOGGER,
    LOGLEVEL,
    Formatter,
    init_logging,
)

__all__ = [
    "CLI",
    "Container",
    "IMAGE_NAME",
    "Formatter",
    "LOGLEVEL",
    "LOGGER",
    "CHANNEL",
    "ERROR",
    "ECHAN",
    "DEBUG",
    "DCHAN",
    "init_logging",
]
