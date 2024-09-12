from pymongo.client_session import ClientSession

from db.types import types
from .collections import domains


def attach_to_entity(
    domain: str,
    target_id: int,
    target_type: types.EntityTargetType,
    session: ClientSession | None = None
) -> None:
    domains.find_one_and_update(
        {"_id": domain},
        {"$set": {
            "target_id": target_id,
            "target_type": target_type
        }},
        session=session,
        upsert=True
    )

def resolve_entity(domain: str, session: ClientSession | None = None) -> types.Entity | None:
    if (entity := domains.find_one({"_id": domain}, session=session)) is None:
        return None
    return types.Entity(**entity)
