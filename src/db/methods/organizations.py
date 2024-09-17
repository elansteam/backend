from pymongo.client_session import ClientSession

from db.types import types
from db.methods.helpers import insert_with_auto_increment_id
from utils.response import ErrorCodes, ErrorResponse
from .collections import organizations

def get(organization_id: int, session: ClientSession | None = None) -> types.Organization | None:
    if (obj := organizations.find_one({"_id": organization_id}, session=session)) is None:
        return None
    return types.Organization(**obj)

def check_existence(organization_id: int, session: ClientSession | None = None) -> bool:
    return organizations.count_documents({"_id": organization_id}, session=session) > 0


def insert_organization_with_id(organization: types.OrganizationWithoutID, session: ClientSession | None = None) -> int:
    return insert_with_auto_increment_id(organizations, organization.db_dump(), session=session)

def add_member(organization_id: int, member: types.Member, session: ClientSession | None = None) -> None:
    if is_user_in_organization(member.id, organization_id):
        raise ErrorResponse(code=ErrorCodes.USER_ALREADY_INVITED)

    organizations.update_one({"_id": organization_id}, {"$push": {"members": member.db_dump()}}, session=session)

def get_organizations_by_user(user_id: int, session: ClientSession | None = None) -> list[types.Organization]:
    return [types.Organization(**org) for org in organizations.aggregate(
        [{"$match": {"members": {"$elemMatch": {"id": user_id}}}}], session=session
    )]

def is_user_in_organization(user_id: int, organization_id: int, session: ClientSession | None = None) -> bool:
    return organizations.count_documents({
        "_id": organization_id, "members": {"$elemMatch": {"id": user_id}}
    }, session=session) > 0
