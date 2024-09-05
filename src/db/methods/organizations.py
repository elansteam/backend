from db.types import types
from db.methods.helpers import insert_with_auto_increment_id
from .collections import organizations


def get(organization_id: int) -> types.Organization | None:
    if (org := organizations.find_one({"_id": organization_id})) is None:
        return None
    return types.Organization(**org)

def insert_organization_with_id(organization: types.OrganizationWithoutID) -> int:
    return insert_with_auto_increment_id(
        organizations, organization.model_dump()
    )

def add_member(organization_id: int, user_id: int) -> None:
    organizations.update_one({"_id": organization_id}, {"$push": {"members": user_id}})
