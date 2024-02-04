"""Database interfaces for some parts of database"""
from db.managers.user_database_manager import UserDatabaseManager
from db.managers.group_database_manager import GroupDatabaseManager
from db.managers.domain_router_database_manager import DomainRouterDatabaseManager
from db.managers.role_database_manager import RoleDatabaseManager

user: UserDatabaseManager = UserDatabaseManager()
group: GroupDatabaseManager = GroupDatabaseManager()
domain: DomainRouterDatabaseManager = DomainRouterDatabaseManager()
role: RoleDatabaseManager = RoleDatabaseManager()
