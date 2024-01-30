"""
Testing micro util functions
"""
import pytest
from auth.utils import has_role_permissions, \
                       gen_code_staff_by_permissions
from auth.utils import Permissions


@pytest.mark.parametrize("data", [
    (Permissions.CREATE_ROLE,),
    (),
    (Permissions.CHANGE_USER_ROLES, Permissions.CREATE_ROLE),
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
