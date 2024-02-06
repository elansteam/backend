"""Group definition"""
from pydantic import BaseModel, Field
from db.models.annotations import IntIdAnnotation, NameAnnotation, DescriptionAnnotation, \
    DomainAnnotation, RoleCodeAnnotation, StrIdAnnotation


class GroupRole(BaseModel):
    """Group role"""

    id: StrIdAnnotation = Field(alias="_id")
    """Group role id"""

    name: NameAnnotation
    """Role name"""

    role_code: RoleCodeAnnotation
    """role code"""

    description: DescriptionAnnotation = Field("")
    """role description"""


class GroupMember(BaseModel):
    """The user's access value generated by several fields"""
    id: IntIdAnnotation = Field(alias="_id")
    """Connected user id"""

    permissions: RoleCodeAnnotation
    """Result role code, that represents final permissions"""

    roles: list[StrIdAnnotation] = Field([])
    """Roles, which member has"""


class Group(BaseModel):
    """Group representation in database"""
    id: IntIdAnnotation = Field(alias='_id')
    """Group id"""

    name: NameAnnotation
    """Group name"""

    description: DescriptionAnnotation = Field("")
    """Group description"""

    domain: DomainAnnotation | None = Field(None)
    """Group domain"""

    members: list[GroupMember] = Field([])
    """Group members"""

    owner: IntIdAnnotation
    """User ID of group owner"""

    roles: list[GroupRole] = Field([])
    """List of names group roles in group"""


class GroupToCreate(BaseModel):
    """Group to create template"""

    name: NameAnnotation

    description: DescriptionAnnotation = Field("")

    domain: DomainAnnotation | None = Field(None)

    members: list[IntIdAnnotation] = Field([])
    """Who will be in group"""
