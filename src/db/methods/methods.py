from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError

from src import types
from .helpers import insert_with_auto_increment_id
from .collections import users, organizations, organization_members


# Organizations
def get_organization(organization_id: int, s: ClientSession | None = None) -> types.Organization | None:
    if (organization := organizations.find_one({"_id": organization_id}, session=s)) is None:
        return None
    return types.Organization(**organization)


def check_organization_existence(organization_id: int, s: ClientSession | None = None) -> bool:
    return organizations.count_documents({"_id": organization_id}, session=s) > 0


def insert_organization(organization: types.OrganizationWithoutID, s: ClientSession | None = None) -> int:
    return insert_with_auto_increment_id(organizations, organization.db_dump(), session=s)


def insert_member_to_organization(member: types.Member, s: ClientSession | None = None) -> bool:
    try:
        organization_members.insert_one(member.db_dump(), session=s)
    except DuplicateKeyError:
        return False
    return True


def get_organizations_by_user(user_id: int, s: ClientSession | None = None) -> list[types.Organization]:

    pipeline = [
        {"$match": {"object_id": user_id}},
        {
            "$lookup": {
                "from": organizations.name,
                "localField": "target_id",
                "foreignField": "_id",
                "as": "organizations",
            }
        },
        {"$unwind": "$organizations"},
        {"$replaceRoot": {"newRoot": "$organizations"}},
    ]
    return [types.Organization(**org) for org in organization_members.aggregate(pipeline, session=s)]


def is_user_in_organization(user_id: int, organization_id: int, s: ClientSession | None = None) -> bool:
    return organization_members.count_documents({"object_id": user_id, "target_id": organization_id}, session=s) > 0


def get_members_of_organization(organization_id: int, s: ClientSession | None = None) -> list[int]:
    pipeline = [
        {"$match": {"target_id": organization_id}},
        {"$group": {"_id": None, "result": {"$push": "$object_id"}}},
    ]
    return next(organization_members.aggregate(pipeline, session=s)).get("result", None)


# Users
def get_user(user_id: int, s: ClientSession | None = None) -> types.User | None:
    if (user := users.find_one({"_id": user_id}, session=s)) is None:
        return None
    return types.User(**user)


def get_user_by_email(email: str, s: ClientSession | None = None):
    if (user := users.find_one({"email": email}, session=s)) is None:
        return None
    return types.User(**user)


def insert_user(user: types.UserWithoutID, s: ClientSession | None = None) -> int | None:
    try:
        return insert_with_auto_increment_id(users, user.db_dump(), session=s)
    except DuplicateKeyError:
        return None


def check_user_existence(user_id: int, s: ClientSession | None = None) -> bool:
    return users.count_documents({"_id": user_id}, session=s) > 0
