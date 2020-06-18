import os

HIDDEN_CONFIG_FOLDER = '~/.py-sim'

def get_config_folder():
    return os.path.expanduser(HIDDEN_CONFIG_FOLDER)

