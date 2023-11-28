"""
Testing micro util functions
"""
# FIXME import system not working
import pytest
from src.auth.utils import (has_role_permissions,
                            gen_code_staff_by_permissions)
from auth.utils import Permissions


@pytest.mark.parametrize("data", [
    (Permissions.C_CREATE_ROLE),
    (),
    (Permissions.C_CREATE_USER, Permissions.C_ADD_USER_TO_GROUP),
    (Permissions.C_CREATE_GROUP,
     Permissions.C_SET_ROLE,
     Permissions.C_ADD_GROUP_ROLE,
     Permissions.C_ADD_USER_TO_GROUP,
     Permissions.C_ADD_ROLE_TO_USER,
     Permissions.C_CREATE_USER)
])
def test_has_role_permission(data: tuple):
    """
    Parametrize test, testing `has_role_permission` function
    Args:
        data: input data
    """

    role_code = gen_code_staff_by_permissions(*data)

    assert has_role_permissions(role_code, *data)

    if len(data) != 0:
        data1 = list(data).pop(-1)

        role_code2 = gen_code_staff_by_permissions(*data1)

        assert not has_role_permissions(role_code2, *data)
