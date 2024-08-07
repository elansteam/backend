from pymongo.errors import DuplicateKeyError

from db import types
from .collections import domains


def reserve_entity(domain: str) -> bool:
    """
    Returns:
        True if ok, else False (domain already used)
    """
    try:
        domains.insert_one({
            "_id": domain,
        })
    except DuplicateKeyError:
        return False
    return True

def attach_to_entity(
    domain: str,
    target_id: int,
    target_type: types.domain.TargetType
) -> None:
    domains.find_one_and_update(
        {"_id": domain},
        {"$set": {
            "target_id": target_id,
            "target_type": target_type
        }},
        upsert=True
    )

def resolve_id(
    domain: str
) -> tuple[int | None, types.domain.TargetType | None]:
    if (entity := domains.find_one({"_id": domain})) is None:
        return None, None
    entity = types.domain.Entity(**entity)
    return entity.target_id, entity.target_type
