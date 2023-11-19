from db.abstract_database_manager import AbstractDatabaseManager
from config import Config
from db.models.grole import GRole


class GRoleDatabaseManager(AbstractDatabaseManager):
    """Group roles database manager"""

    collection_name = Config.Collections.groles

    async def get_by_name(self, grole_name: str, group_name: str) -> GRole | None:
        """Get group role by name

        Args:
            grole_name (str): group role name
            group_name (str): group name

        Returns:
            GRole | None: group role or None
        """
        grole = await self.db.find_one({"name": grole_name, "group": group_name})

        if grole is None:
            return None

        return GRole(**grole)

    async def create(self, grole: GRole) -> None:
        """Insert new role to the database

        Args:
            grole (GRole): _description_
        """
        await self.db.insert_one({**grole.model_dump()})
