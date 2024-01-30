"""Database interfaces for some parts of database"""
from src.db.managers.user_database_manager import UserDatabaseManager
from src.db.managers.group_database_manager import GroupDatabaseManager
from src.db.managers.domain_router_database_manager import DomainRouterDatabaseManager

user = UserDatabaseManager()
group = GroupDatabaseManager()
domain = DomainRouterDatabaseManager()
