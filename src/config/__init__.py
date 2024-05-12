"""Project configuration"""
import os
import sys
from loguru import logger
from pydantic import ValidationError

from . import config_model


_CONFIG_PATH_ENV_VARIABLE_NAME = "ELANTS_CONFIG_FILE_PATH"

_config_path = os.getenv(_CONFIG_PATH_ENV_VARIABLE_NAME)

if _config_path is None:  # check for existing env variable
    logger.error(
        f"Environment variable {_CONFIG_PATH_ENV_VARIABLE_NAME} is not set"
    )
    sys.exit(1)

def _check_json_file(file_path: str) -> bool:
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

if not _check_json_file(_config_path):  # check_json_file
    logger.error(
        f"File {_config_path} is not a json file or isnt exists"
    )
    sys.exit(1)

def _load_config() -> config_model.Config:
    """parse && validate config file"""
    try:
        with open(_config_path, "r", encoding="utf-8") as config_file:
            return config_model.Config.model_validate_json(config_file.read())
    except ValidationError as exception:
        logger.error(
            f"Failed to load configuration from file {_config_path}: {exception}"
        )
        sys.exit(1)

logger.info(f"Loading configuration from file {_config_path}")
config = _load_config()

logger.info(f"Successfully loaded configuration from file {_config_path}")
if config.show_config:
    logger.info(f"Current configuration: {config.model_dump_json(indent=4)}")
