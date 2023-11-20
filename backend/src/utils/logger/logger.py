from logging import config, getLogger
from pathlib import Path
from src.utils.yaml.yaml import load_yaml

logging_config = None

def load_logging_config():
    global logging_config

    if logging_config is None:
        file_path = Path.joinpath(Path(__file__).parent, '..', '..', 'settings.yaml') 
        config.dictConfig(load_yaml(file_path)['logger'])
        logging_config = True

def get_logger(path: str):
    load_logging_config()
    return getLogger(path)