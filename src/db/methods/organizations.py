from db.types import types
from .collections import organizations


def get(org_id: int) -> types.Organization | None:
    if (org := organizations.find_one({"_id": org_id})) is None:
        return None
    return types.Organization(**org)

