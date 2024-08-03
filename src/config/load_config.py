import os
import sys
from loguru import logger
from pydantic import ValidationError

from .config_model import Config

CONFIG_PATH_ENV_VARIABLE_NAME = "CONFIG_PATH"

def load_config() -> Config:
    config_path = os.getenv(CONFIG_PATH_ENV_VARIABLE_NAME)

    if config_path is None:
        logger.error("Environment variable {_CONFIG_PATH_ENV_VARIABLE_NAME} is not set")
        sys.exit(1)

    file_exists = False
    if os.path.exists(config_path) and os.path.isfile(config_path):
        _, file_extension = os.path.splitext(config_path)
        if file_extension.lower() == '.json':
            file_exists = True

    if not file_exists:
        logger.error(
            f"File {config_path} is not a json file or isnt exists"
        )
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            return Config.model_validate_json(config_file.read())
    except ValidationError as exception:
        logger.error(
            f"Failed to load configuration from file {config_path}: {exception}"
        )
        sys.exit(1)
