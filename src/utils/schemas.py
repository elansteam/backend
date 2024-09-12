from typing import Any
import pydantic


class BaseModel(pydantic.BaseModel):
    def db_dump(self, *args, **kwargs) -> dict[str, Any]:
        return self.model_dump(by_alias=True, *args, **kwargs)

    model_config = pydantic.ConfigDict(populate_by_name=True)
