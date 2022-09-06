import os

from monitor.settings import load_settings


def pytest_configure(config):
    os.environ["ENV_FILE"] = "unittest.env"
    load_settings(os.environ["ENV_FILE"])
