import os


def pytest_configure(config):
    os.environ['ENV_FILE'] = 'e2e.env'
