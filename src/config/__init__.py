"""Project configuration"""
import os
import sys
from loguru import logger


from . import config_model

CONFIG_PATH_ENV_VARIABLE_NAME = "ELANTS_CONFIG_FILE_PATH"

config_path = os.getenv(CONFIG_PATH_ENV_VARIABLE_NAME)

if config_path is None:  # check for existing env variable
    logger.error(
        f"Environment variable {CONFIG_PATH_ENV_VARIABLE_NAME} is not set"
    )
    sys.exit(1)

def check_json_file(file_path: str) -> bool:
    """Check that file_path is a json file and exists

    Args:
        file_path: file to check

    Returns:
        True if file_path is a json file and exists, False otherwise
    """
    if os.path.exists(file_path) and os.path.isfile(file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.json':
            return True
    return False

if not check_json_file(config_path):  # check_json_file
    logger.error(
        f"File {config_path} is not a json file or isnt exists"
    )
    sys.exit(1)

logger.info(f"Loading configuration from file {CONFIG_PATH_ENV_VARIABLE_NAME}")

with open(config_path, "r", encoding="utf-8") as config_file:  # parse && validate config file
    config: config_model.Config = config_model.Config.model_validate_json(config_file.read())

logger.info(f"Successfully loaded configuration from file {CONFIG_PATH_ENV_VARIABLE_NAME}")
logger.info(f"Current configuration: {config.model_dump_json(indent=4)}")
