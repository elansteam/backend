from pydantic import BaseModel, field_validator, ValidationError


class Role(BaseModel):
    """Представление роли пользователя, роль - совокупность permissions"""

    name: str
    """Уникальное имя роли"""

    description: str
    """Описание роли"""

    permissions: int
    """32 битное число, двоичная запись которого кодирует permissions"""

    @field_validator("permissions")
    def my_custom_validator(cls, value):
        if value < 0:
            raise ValidationError("Permissions must be positive")
        return value