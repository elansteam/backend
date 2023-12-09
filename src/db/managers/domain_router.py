"""Domain router definition"""
from db.abstract_database_manager import AbstractDatabaseManager
from db.models.domain_node import DomainNode
from config import Config
from bson.objectid import ObjectId


class DomainRouter(AbstractDatabaseManager):
    """Routing and manage object namas"""

    collection_name = Config.Collections.domain_router

    def get_domain_node(self, target_name: str) -> DomainNode | None:
        """
        Getting the domain node by target object name
        Args:
            target_name: target object name
        Returns:
            DomainNode or None of not found
        """
        raise NotImplementedError  # FIXME

    def raname_domain_node(self, target_name: str, replace_name: str) -> None:
        """
        Rename domain node
        Args:
            target_name: target object name
            replace_name: replacing name
        """
        raise NotImplementedError  # FIXME
