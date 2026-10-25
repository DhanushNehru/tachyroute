import logging

from tachyroute.router import Router
from tachyroute.engine import Engine

__all__ = ["Router", "Engine"]
__version__ = "0.1.1"

# Library best practice: stay silent unless the application configures logging.
logging.getLogger(__name__).addHandler(logging.NullHandler())
