import os

from monitor import settings


def load_settings(env_file=None):
    env_file = env_file or os.environ.get('ENV_FILE')
    settings.load_settings(env_file)
