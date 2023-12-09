"""
Testing micro util functions
"""
import pytest
from src.auth.utils import (has_role_permissions,
                            gen_code_staff_by_permissions)
from auth.utils import Permissions


@pytest.mark.parametrize("data", [
    (Permissions.CAN_CREATE_ROLE,),
    (),
    (Permissions.CAN_CREATE_USER, Permissions.CAN_ADD_USER_TO_GROUP),
    (Permissions.CAN_CREATE_GROUP,
     Permissions.CAN_SET_ROLE,
     Permissions.CAN_ADD_GROUP_ROLE,
     Permissions.CAN_ADD_USER_TO_GROUP,
     Permissions.CAN_ADD_ROLE_TO_USER,
     Permissions.CAN_CREATE_USER)
])
def test_has_role_permission(data: tuple[Permissions]):
    """
    Parametrize test, testing `has_role_permission` function
    Args:
        data: input data
    """

    role_code = gen_code_staff_by_permissions(*data)

    assert has_role_permissions(role_code, *data)

    if len(data) != 0:
        data1 = list(data)
        data1.pop(-1)

        role_code2 = gen_code_staff_by_permissions(*data1)

        assert not has_role_permissions(role_code2, *data)
