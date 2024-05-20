"""Methods to work with domains"""

from loguru import logger
from pymongo.errors import DuplicateKeyError

from db.models import Entity
from db.annotations import DomainAnnotation
from .collections import domains


def reserve(domain: DomainAnnotation) -> bool:
    """ 
    Reserving domain for some entity with unknown type and id
    Returns:
        True if reserve was successful, else False
    """
    to_reserve = Entity(
        _id=domain,
        entity_type="reserve"
    )

    try:
        domains.insert_one(to_reserve.model_dump(by_alias=True))
        logger.debug(f"Reserve entity <{domain}>")
    except DuplicateKeyError:
        return False

    return True

def delete(domain: DomainAnnotation):
    """
    Deleting entity by domain
    Args:
        domain: domain
    """
    domains.delete_one({"_id": domain})
    logger.info(f"Deleted entity <{domain}>")
