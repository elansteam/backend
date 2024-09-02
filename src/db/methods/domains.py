from db.types import types
from .collections import domains


def attach_to_entity(
    domain: str,
    target_id: int,
    target_type: types.EntityTargetType
) -> None:
    domains.find_one_and_update(
        {"_id": domain},
        {"$set": {
            "target_id": target_id,
            "target_type": target_type
        }},
        upsert=True
    )

def resolve_entity(domain: str) -> types.Entity | None:
    if (entity := domains.find_one({"_id": domain})) is None:
        return None
    return types.Entity(**entity)
