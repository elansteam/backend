from pymongo.errors import DuplicateKeyError

from db import types
from db.types.common import IntegerId, DomainName
from .collections import domains


def reserve_entity(domain: DomainName) -> bool:
    """Creates entity with type None for domain
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
    domain: DomainName,
    target_id: IntegerId,
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
    domain: DomainName,
    target_type: types.domain.TargetType
) -> IntegerId | None:
    entity = domains.find_one({"_id": domain, "target_type": target_type})

    if entity is None:
        return None
    return types.domain.Entity(**entity).target_id
