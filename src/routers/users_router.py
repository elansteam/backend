"""Users endpoints"""
from fastapi import APIRouter, Depends

router = APIRouter()

# @router.post(
#     "/add_role",
#     response_model=Role,
#     responses={
#         400: get_error_schema("Failed to add role to user")
#     }
# )
# async def add_role_to_user(user_id: int, role_id: str,
#                            _current_user: User = Depends(auth_user(
#                                Permissions.CAN_ADD_ROLE_TO_USER
#                            ))):
#     """Adding role to user"""
#     user_to_add = await db.user.get(user_id)
#
#     if user_to_add is None:
#         return get_error_response(f"User with id {user_id} doesn't exist")
#
#     role = await db.role.get(role_id)
#
#     if role is None:
#         return get_error_response(f"Role with id <{role_id}> doesn't exist")
#
#     if role_id in user_to_add.roles:
#         return get_error_response(
#             f"Role with id <{role_id}> already exists for user with id <{user_id}>"
#         )
#
#     await db.user.add_role(user_id, role_id)
#     return role
