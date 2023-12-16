"""Database interfaces for some parts of database"""
from db.managers.user_database_manager import UserDatabaseManager
from db.managers.group_role_database_manager import GroupRoleDatabaseManager
from db.managers.role_database_manager import RoleDatabaseManager
from db.managers.group_database_manager import GroupDatabaseManager
from db.managers.domain_router_database_manager import DomainRouterDatabaseManager

user = UserDatabaseManager()
group = GroupDatabaseManager()
group_role = GroupRoleDatabaseManager()
role = RoleDatabaseManager()
domain = DomainRouterDatabaseManager()
