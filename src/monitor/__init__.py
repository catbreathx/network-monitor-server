import logging.config

import yaml

from . import authentication
from . import database
from . import exceptions
from . import middleware
from . import repository
from . import route
from . import schema
from . import service
from . import settings


def initialize_logging():
    with open("logging.yml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    logging.config.dictConfig(config)
