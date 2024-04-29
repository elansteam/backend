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



# class Config:
#     """Entire project config"""
#     if any(arg_value is None for arg_value in [
#         os.environ.get("DB_CONNECT_URL"),
#         os.environ.get("DB_NAME"),
#         os.environ.get("COLLECTION_USERS"),
#         os.environ.get("COLLECTION_ROLES"),
#         os.environ.get("COLLECTION_GROUP_ROLES"),
#         os.environ.get("COLLECTION_GROUPS"),
#         os.environ.get("COLLECTION_DOMAIN"),
#         os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
#         os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"),
#         os.environ.get("ALGORITHM"),
#         os.environ.get("JWT_SECRET_KEY"),
#         os.environ.get("JWT_REFRESH_SECRET_KEY"),
#         os.environ.get("APP_TITLE")
#     ]):
#         logger.error([
#             os.environ.get("DB_CONNECT_URL"),
#             os.environ.get("DB_NAME"),
#             os.environ.get("COLLECTION_USERS"),
#             os.environ.get("COLLECTION_ROLES"),
#             os.environ.get("COLLECTION_GROUP_ROLES"),
#             os.environ.get("COLLECTION_GROUPS"),
#             os.environ.get("COLLECTION_DOMAIN"),
#             os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
#             os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"),
#             os.environ.get("ALGORITHM"),
#             os.environ.get("JWT_SECRET_KEY"),
#             os.environ.get("JWT_REFRESH_SECRET_KEY"),
#             os.environ.get("APP_TITLE")
#         ])
#         sys.exit(1)
#     db_connect_url: str = os.environ.get("DB_CONNECT_URL") or ""

#     db_name: str = os.environ.get("DB_NAME") or ""

#     class Collections:
#         """Collection db names"""
#         users = os.environ.get("COLLECTION_USERS") or ""
#         roles = os.environ.get("COLLECTION_ROLES") or ""
#         group_roles = os.environ.get("COLLECTION_GROUP_ROLES") or ""
#         groups = os.environ.get("COLLECTION_GROUPS") or ""
#         domain_router = os.environ.get("COLLECTION_DOMAIN") or ""
#         internal_counters = os.environ.get("COLLECTION_INTERNAL_COUNTERS") or ""
#         contests = os.environ.get("COLLECTION_CONTESTS") or ""
#         problems = os.environ.get("COLLECTION_PROBLEMS") or ""
#         submissions = os.environ.get("COLLECTION_SUBMISSIONS") or ""

#     class Auth:
#         """Data for auth system"""
#         ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES") or "")
#         REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES") or "")
#         ALGORITHM = os.environ.get("ALGORITHM") or ""

#         JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or ""
#         JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY") or ""

#     app_title = os.environ.get("APP_TITLE") or ""
#     elan_path = os.environ.get("ELAN_PATH") or "/ELAN"  # FIXME NOT USED or user idk

#     # FIXME it may not work later
#     rabbitmq_main_queue = os.environ.get("RABBITMQ_MAIN_QUEUE") or "INVOKER"
