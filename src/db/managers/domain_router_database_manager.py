"""DomainRouterDatabaseManager definition"""
from db.helpers.abstract_database_manager import AbstractDatabaseManager
from config import Config
from db.models.entity import Entity


class DomainRouterDatabaseManager(AbstractDatabaseManager):
    """Database methods to routing domains"""

    collection_name = Config.Collections.name_router

    async def resolve(self, domain: str) -> Entity | None:
        """
        Resolving domain to entity type and id
        Args:
            name: the name to resolve
        Returns:
            id or None if not found
        """
        res = await self.collection.find_one({"_id": domain})
        if res is None:
            return None
        return Entity(**res)
