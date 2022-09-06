import logging.config

import yaml


def initialize_logging():
    with open("logging.yml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    logging.config.dictConfig(config)
