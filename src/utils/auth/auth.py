# TODO: REFACTOR
# """
# Helpers for auth stuff
# """

# import datetime
# import jose.jwt
# from loguru import logger
# from passlib.context import CryptContext
# from fastapi import Header
# from starlette import status as http_status

# from db import methods
# from db.types.user import User
# from db.types.common import RoleCode
# from utils import response
# from config import config
# from .permissions import Permissions


# password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def has_role_permissions(
#     role_code: RoleCode,
#     *permissions: Permissions
# ) -> bool:
#     """Checking if this role has permissions
#     Args:
#         role_code: representation permissions through converted to bits int32 number

#     Returns:
#         True - if role has permission, else False
#     """
#     for perm in permissions:
#         if (role_code >> perm.value) % 2 == 0:
#             return False
#     return True

# def generate_role_code(*permissions: Permissions) -> RoleCode:
#     """
#     Generate role code by permissions
#     Args:
#         *permissions: permissions, which should be contained in role code
#     Returns:
#         role code
#     """
#     role_code = 0
#     for perm in permissions:
#         role_code += 1 << perm.value

#     return role_code

# def hash_password(password: str) -> str:
#     return password_context.hash(password)

# def verify_password(password: str, hashed_password: str) -> bool:
#     return password_context.verify(password, hashed_password)

# def create_jwt(
#         subject: str,
#         expiration_time_minutes: int
# ) -> str:
#     """Create a JWT from a subject with expiration time in minutes

#     Args:
#         subject: Data to encode
#         expiration_time_minutes: Token expiration time

#     Returns:
#         JWT as string
#     """

#     expiration_time = datetime.datetime.utcnow() + datetime.timedelta(
#         minutes=expiration_time_minutes
#     )

#     # ! it is neccessary to name field like "exp" and "sub"
#     to_encode = {
#         "exp": expiration_time,
#         "sub": subject
#     }

#     created_jwt = jose.jwt.encode(
#         to_encode,
#         config.auth.jwt_access_secret_key.get_secret_value(),
#         algorithm=config.auth.algorithm
#     )
#     return created_jwt

# def get_user_by_access_jwt(jwt: str) -> User:
#     """Get current user by access token or raise ErrorResponse
#     Args:
#         jwt: access token
#     Raises:
#         ErrorResponse: Raise 401 error if access token is invalid
#     Returns:
#         User: user object
#     """
#     try:
#         payload = jose.jwt.decode(
#             jwt,
#             config.auth.jwt_access_secret_key.get_secret_value(),
#             algorithms=[config.auth.algorithm]
#         )
#         token_sub = payload["sub"]

#     except jose.ExpiredSignatureError as exc:
#         raise response.ErrorResponse(
#             code=response.ErrorCodes.TOKEN_EXPIRED,
#             message="Token signature expired",
#             http_status_code=http_status.HTTP_401_UNAUTHORIZED,
#         ) from exc
#     except Exception as exc:
#         raise response.ErrorResponse(
#             code=response.ErrorCodes.TOKEN_VALIDATION_FAILED,
#             message="Token validation failed",
#             http_status_code=http_status.HTTP_401_UNAUTHORIZED,
#         ) from exc

#     user = methods.users.get(int(token_sub))

#     if user is None:
#         raise response.ErrorResponse(
#             code=response.ErrorCodes.COULD_NOT_FIND_USER_BY_TOKEN,
#             message="Could not find user by this token",
#             http_status_code=http_status.HTTP_401_UNAUTHORIZED,
#         )

#     return user

# def auth_user(*permissions: Permissions):
#     """
#     Dependency, that authorize user with given permissions by jwt token in
#     Authorization header.

#     Usage example:
#     >>> def endpoint(user: User = Depends(auth_user(Permissions.CREATE_ROLE)))
#     Args:
#         *permissions: Permissions, which must contain user roles
#     Returns:
#         Function that auth user by given permissions and auth header
#     """

#     def wrapper(authorization: str = Header()) -> User:
#         """
#         Authorization user by given permissions and auth header.
#         Args:
#             authorization: Authorization header in format: Bearer <auth_token>
#         Returns:
#             Authorized user object
#         Raises:
#             ErrorResponse: validation error or access denied
#         """
#         credentials = authorization.split()
#         if len(credentials) != 2:
#             raise response.ErrorResponse(
#                 code=response.ErrorCodes.INCORRECT_AUTH_HEADER_FOMAT,
#                 http_status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 message="Incorrect authorization header format. Format: Bearer <auth>"
#             )

#         bearer, token, *_ = *credentials, None

#         if bearer != "Bearer" or token is None:
#             raise response.ErrorResponse(
#                 code=response.ErrorCodes.INCORRECT_AUTH_HEADER_FOMAT,
#                 http_status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 message="Incorrect authorization header format. Format: Bearer <auth>"
#             )

#         user = get_user_by_access_jwt(token)

#         permissions_mask = 0

#         for role_name in user.roles:
#             role = methods.roles.get(role_name)
#             if role is None:
#                 logger.error(f"Role with name <{role_name}> not found")
#                 continue
#             permissions_mask |= role.role_code

#         if not has_role_permissions(
#             permissions_mask,
#             *permissions
#         ):
#             required_permissions = []

#             for permission in permissions:
#                 if not has_role_permissions(permissions_mask, permission):
#                     required_permissions.append(permission.name)

#             raise response.ErrorResponse(
#                 code=response.ErrorCodes.ACCESS_DENIED,
#                 http_status_code=http_status.HTTP_403_FORBIDDEN,
#                 message=f"Missing permissions: {' '.join(required_permissions)}"
#             )
#         return user
#     return wrapper
