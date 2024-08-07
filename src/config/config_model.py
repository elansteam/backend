"""Entire project configuration model"""
from pydantic import BaseModel, SecretStr

class MongoDBCollections(BaseModel):
    users: str = "Users"
    domains: str = "Domains"
    groups: str = "Groups"
    group_roles: str = "GroupRoles"
    roles: str = "Roles"
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

class Config(BaseModel):
    database: DatabaseConfig
    auth: AuthConfig
    debug: bool = False
    allow_origins: list[str] = []
