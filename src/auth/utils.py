"""
Helpers for auth stuff
"""

from passlib.context import CryptContext
from db.models.user import User
from db.annotations import RoleCodeAnnotation
from auth.permissions import Permissions

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_role_code_for_permissions(
    role_code: RoleCodeAnnotation,
    *permissions: Permissions
) -> bool:
    """Checking if this role has permissions
    Args:
        role_code: representation permissions through converted to bits int32 number

    Returns:
        True - if role has permission, else False
    """

    for perm in permissions:
        if (role_code >> perm.value) % 2 == 0:
            return False
    return True


def generate_role_code(*permissions: Permissions) -> RoleCodeAnnotation:
    """
    Generate role code by permissions
    Args:
        *permissions: permissions, which should be contained in role code
    Returns:
        role code
    """
    role_code = 0
    for perm in permissions:
        role_code += 1 << perm.value

    return role_code


def hash_password(password: str) -> str:
    """
    Hashing password
    Args:
        password: password to hash

    Returns:
        hashed password
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Checks what hashed password is password
    Args:
        password: password
        hashed_password: password hash

    Returns:
        True if hash(password) equal to hashed_password, else False
    """
    return password_context.verify(password, hashed_password)


def create_JWT(
        subject: str, is_access=True, expires_delta: int | None = None
) -> str:
    ...


async def get_current_user(token: str) -> User:
    """Get current user by access token or raise HTTPException
    Args:
        token (str): access token
    Raises:
        AuthException: Raise 401 error if access token is invalid
    Returns:
        User: user object
    """
    ...


def auth_user(*permissions: Permissions):
    """
    Decorator
    Use:
    >>> def endpoint(user: User = Depends(auth_user(Permissions.CREATE_ROLE)))
    Auth user by permissions.
    Args:
        *permissions: Permissions, which must contain user roles
    Returns:
        function, which auth user
    Raises:
        AuthException: Raise 403 error user hasn`t permissions
    """
    ...
