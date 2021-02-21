import os
import yaml

from utils.logging_utils import create_default_logger

logger = create_default_logger(__file__)

def load_config(config_file=os.path.dirname(__file__) + '/../config.yml'):
    """Load configurations from yaml file

    Args:
        config_file (string, optional): Configurations file path. Defaults to os.path.dirname(__file__)+'/../configs.yml'.

    Raises:
        FileNotFoundError: Configuration file not found.

    Returns:
        dict: Configurations
    """
    if (os.path.isfile(config_file)):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    else:
        raise FileNotFoundError(("File not found: config.yml"))
    
    logger.debug("Configurations loaded successfully")

    return cfg

config = load_config()