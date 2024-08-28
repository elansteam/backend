"""Entire project configuration model"""
import os
import sys
from pydantic import BaseModel, SecretStr
from pydantic import ValidationError
from loguru import logger


class MongoDBCollections(BaseModel):
    users: str = "Users"
    domains: str = "Domains"
    groups: str = "Groups"
    group_roles: str = "GroupRoles"
    internal_counters: str = "InternalCounters"
    group_members: str = "GroupMembers"
    contests: str = "Contests"

class DatabaseConfig(BaseModel):
    connect_url: SecretStr
    name: str
    collections: MongoDBCollections = MongoDBCollections()

class AuthConfig(BaseModel):
    access_token_expire_minutes: int = 10
    refresh_token_expire_minutes: int = 7 * 24 * 60
    jwt_access_secret_key: SecretStr
    jwt_refresh_secret_key: SecretStr
    service_token: SecretStr

class Config(BaseModel):
    database: DatabaseConfig
    auth: AuthConfig
    debug: bool = False
    allow_origins: list[str] = []

    @classmethod
    def load(cls):
        config_path = os.getenv("CONFIG_PATH")

        if config_path is None:
            logger.error("Environment variable CONFIG_PATH is not set")
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
                f"Failed to load configuration with errors: {exception.errors()}"
            )
            sys.exit(1)
