from loguru import logger

import db
import utils.auth
from config import config


def create_super_user():
    admin_role = db.types.role.Role(
        _id="admin",
        name="Admin",
        code=utils.auth.permissions.ALL_PERMISSIONS_ROLE_CODE,
        description="The most powerful thing besides database access credentials))"
    )
    if db.methods.roles.insert(admin_role):
        logger.info("Created admin role")

    result = db.methods.users.insert_user_document_with_id({
        "email": config.super_user.email,
        "hashed_password": utils.auth.hash_password(config.super_user.password.get_secret_value()),
        "roles": ["admin"]
    })
    if result is not None:
        logger.info("Created a new super user")

    super_user = db.methods.users.get_by_email(config.super_user.email)
    if super_user is None:
        logger.warning("There is no super user in the system")
    else:
        logger.info(f"Current super user: id={super_user.id}, email={super_user.email}")
