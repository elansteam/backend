from pydantic import BaseModel, field_validator, ValidationError


class GRole(BaseModel):
    """Представление роли конкретно в группе"""

    name: str
    """Имя роли"""

    description: str = ""
    """Описание роли"""

    gpermissions: int
    """Список разрешений"""

    group: str
    """Группа, к которой привязана grole"""

    @field_validator("gpermissions")
    def my_custom_validator(cls, value):
        if value < 0:
            raise ValidationError("GPermissions must be positive")
