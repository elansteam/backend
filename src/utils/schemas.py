from typing import Any
import pydantic


class BaseModel(pydantic.BaseModel):
    def model_dump(self, by_alias=True, **kwargs) -> dict[str, Any]:
        return super().model_dump(by_alias=by_alias, **kwargs)
