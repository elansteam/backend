"""Database interfaces for some parts of database"""
from managers.user_database_manager import UserDatabaseManager
from managers.group_role_database_manager import GroupRoleDatabaseManager
from managers.role_database_manager import RoleDatabaseManager
from managers.group_database_manager import GroupDatabaseManager

user = UserDatabaseManager()
group = GroupDatabaseManager()
group_role = GroupRoleDatabaseManager()
role = RoleDatabaseManager()
