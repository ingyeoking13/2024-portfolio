from logging import config, getLogger
from pathlib import Path
from src.utils.yaml.yaml import load_settings

logging_config = None

def load_logging_config(_config = None):
    global logging_config

    if logging_config is None:
        if _config is None:
            config.dictConfig(load_settings()['logger'])
            logging_config = True
        if _config == 'ray':
            config.dictConfig(load_settings()['ray']['logger'])
            logging_config = True

def get_logger(path: str, config=None):
    load_logging_config(config)
    return getLogger(path)