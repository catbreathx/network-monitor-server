import os
from glob import glob

from monitor.settings import load_settings

pytest_plugins = [
    fixture_file.replace("/", ".").replace(".py", "")
    for fixture_file in glob("tests/unit/fixtures/*.py", recursive=True)
]


def pytest_configure(config):
    os.environ["ENV_FILE"] = "unittest.env"
    load_settings(os.environ["ENV_FILE"])
