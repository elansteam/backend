from typing import Any
import pydantic
import pydantic.decorator


class BaseModel(pydantic.BaseModel):
    def model_dump(self, by_alias=True, **kwargs) -> dict[str, Any]:
        return super().model_dump(by_alias=by_alias, **kwargs)

    def db_dump(self, by_alias=True, **kwargs) -> dict[str, Any]:
        result = self.model_dump(by_alias=by_alias, **kwargs)
        if "id" in result:
            result["_id"] = result.pop("id")
        return result

    @pydantic.model_validator(mode="before")
    def convert_id(cls, values):
        if "_id" in values:
            values["id"] = str(values.pop("_id"))
        return values
