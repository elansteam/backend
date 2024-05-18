"""
Helpers for auth stuff
"""

from passlib.context import CryptContext
from db.models.user import User
from auth.permissions import Permissions

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(Exception):
    """Custom exception for auth errors"""
    status: str
    status_code: int
    response: dict

    def __init__(self, status: str, status_code: int, response: dict | None = None):
        self.status = status
        self.status_code = status_code
        if response is None:
            self.response = {}
        else:
            self.response = response


def has_role_permissions(role_staff: int, *permissions: Permissions) -> bool:
    """Check what role contains permissions
    Args:
        role_staff: representation permissions through converted to bits int32 number

    Returns:
        True - if role has permission, else False
    """

    for perm in permissions:
        if (role_staff >> perm.value) % 2 == 0:
            return False

    return True


def gen_code_staff_by_permissions(*permissions: Permissions) -> int:
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


def get_hashed_password(password: str) -> str:
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


def create_token(
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
