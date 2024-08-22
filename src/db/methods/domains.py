from db import types
from .collections import domains


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

def resolve_entity(domain: str) -> types.domain.Entity | None:
    if (entity := domains.find_one({"_id": domain})) is None:
        return None
    return types.domain.Entity(**entity)
