from logging import config, getLogger
from pathlib import Path
from src.utils.yaml.yaml import load_settings

logging_config = None

def load_logging_config():
    global logging_config

    if logging_config is None:
        config.dictConfig(load_settings()['logger'])
        logging_config = True

def get_logger(path: str):
    load_logging_config()
    return getLogger(path)