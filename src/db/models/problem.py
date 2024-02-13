from pydantic import BaseModel, Field
from db.models.annotations import IntIdAnnotation, NameAnnotation


class Problem(BaseModel):
    """Problem representation"""

    id: IntIdAnnotation = Field(alias='_id')

    name: NameAnnotation

    # TODO: add tags and other
