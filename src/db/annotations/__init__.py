"""Annotations for BaseModels fields"""
from typing import Annotated
from pydantic import AfterValidator
from db.annotations import validators

# this is annotations. They can be use in typehints
IntIdAnnotation = Annotated[int, AfterValidator(validators.positive_number)]
EmailAnnotation = Annotated[str, AfterValidator(validators.email_string)]
DomainAnnotation = Annotated[str, AfterValidator(validators.domain_name)]
NameAnnotation = Annotated[str, AfterValidator(validators.name_string)]
DescriptionAnnotation = Annotated[str, AfterValidator(validators.description_string)]
RoleCodeAnnotation = Annotated[int, AfterValidator(validators.not_negative_number)]
StrIdAnnotation = Annotated[str, AfterValidator(validators.string_id)]
StrIntIdAnnotation = Annotated[str, AfterValidator(validators.string_positive_number)]
