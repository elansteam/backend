from pymongo.client_session import ClientSession

from db.types import types
from .helpers import get_related_collection


def get_object_by_id[T: types.DocumentWithIntId](
    object_id: int, object_type: type[T], session: ClientSession | None = None,
) -> T | None:
    if (obj := get_related_collection(object_type).find_one({"_id": object_id}, session=session)) is None:
        return None
    return object_type(**obj)

def check_object_existence(
    object_id: int, object_type: type[types.DocumentWithIntId], session: ClientSession | None = None,
) -> bool:
    return get_related_collection(object_type).count_documents({"_id": object_id}, session=session) > 0
