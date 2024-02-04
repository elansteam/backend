"""DomainRouterDatabaseManager definition"""
from pymongo.errors import DuplicateKeyError

from config import Config
from db.models.entity import Entity
from db.helpers.abstract_database_manager import AbstractDatabaseManager


class DomainRouterDatabaseManager(AbstractDatabaseManager):
    """Database methods to routing domains"""

    collection_name = Config.Collections.domain_router

    async def resolve(self, domain: str) -> Entity | None:
        """
        Resolving domain to entity type and id
        Args:
            domain: the name to resolve
        Returns:
            id or None if not found
        """
        res = await self.collection.find_one({"_id": domain})
        if res is None:
            return None
        return Entity(**res)

    async def resolve_id(self, domain: str, entity_type: str) -> int | None:
        """
        Resolving entity by domain with type and id
        Args:
            domain: domain to resolve
            entity_type: entity type to resolve
        Returns:
            entity_id if entity has type == entity_type, else return None
        """

        res = await self.resolve(domain)
        if res is None:
            return None
        if res.entity_type != entity_type:
            return None
        return res.entity_id

    async def reserve(self, domain: str) -> bool:
        """
        Reserving domain for some entity with unknown type and id
        Returns:
            True if reserve was successful, else False
        """
        to_reserve = Entity(
            _id=domain,
            entity_type="reserve",
        )

        try:
            await self.collection.insert_one(to_reserve.model_dump(by_alias=True))
        except DuplicateKeyError:
            return False

        return True

    async def attach(self, domain: str, entity_type: str, entity_id: int) -> None:
        """
        Attaching entity to existing reserved entity. Defined entity type and id
        Args:
            domain: Domain attach to
            entity_type: attaching entity type
            entity_id: attaching entity id
        """

        await self.collection.find_one_and_update({"_id": domain}, {"$set": {
            "entity_type": entity_type,
            "entity_id": entity_id
        }}, upsert=True)
