"""Define configuration class"""
from pydantic import BaseModel, SecretStr


class MongoDBCollections(BaseModel):
    """List of all collections in database"""
    users: str
    domains: str
    groups: str
    group_roles: str
    roles: str

class DatabaseConfig(BaseModel):
    """Database configuration"""
    connect_url: SecretStr
    name: str
    collections: MongoDBCollections

class AuthConfig(BaseModel):
    """Auth configuration"""
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    jwt_access_secret_key: SecretStr
    jwt_refresh_secret_key: SecretStr

class RabbitMQConfig(BaseModel):
    """Config for RabbitMQ"""
    connect_url: SecretStr
    # TODO: insert other necessary fields later

class Config(BaseModel):
    """Entire project configuration"""
    database: DatabaseConfig
    rabbitmq: RabbitMQConfig
    auth: AuthConfig
    app_title: str
