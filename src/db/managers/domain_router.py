"""Domain router definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.domain_node import DomainNode
from config import Config
from utils.utils import ObjectId


class DomainRouter(AbstractDatabaseManager):
    """Routing and manage object namas"""

    collection_name = Config.Collections.domain_router

    async def get_by_id(self, _id: ObjectId) -> DomainNode | None:
        """
        Getting the domain node by id
        Args:
            _id: domain node id

        Returns:
            DomainNode or None of not found
        """
        raise NotImplementedError  # FIXME

    async def get_by_target_name(self, target_name: str) -> DomainNode | None:
        """
        Getting the domain node by target object name
        Args:
            target_name: target object name
        Returns:
            DomainNode or None of not found
        """
        raise NotImplementedError  # FIXME

    async def get_by_target_id(self, target_id: ObjectId) -> DomainNode | None:
        """
        Getting the domain node by target object id
        Args:
            target_id: target object id
        Returns:
            DomainNode or None of not found
        """
        raise NotImplementedError  # FIXME

    async def rename_target(self, _id: ObjectId, new_name: str) -> bool:
        """
        Renaming node target by own node id
        Args:
            _id: domain node id
            new_name: new node id
        Returns:
            True if the node was renamed successfully, else False
        """
        raise NotImplementedError  # FIXME

    async def create(self, domain_node: DomainNode) -> bool:
        """
        Creating a new domain node
        Args:
            domain_node: node to create

        Returns:
            True if the object was created successfully, else False
        """
        raise NotImplementedError  # FIXME
