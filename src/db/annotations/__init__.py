"""Annotations for BaseModels fields"""
from typing import Annotated
from pydantic import AfterValidator
from db.annotations import validators

# this is annotations. They can be use in typehints
StrIdAnnotation = Annotated[str, AfterValidator(validators.string_id)]
NameAnnotation = Annotated[str, AfterValidator(validators.name_string)]
EmailAnnotation = Annotated[str, AfterValidator(validators.email_string)]
DomainAnnotation = Annotated[str, AfterValidator(validators.domain_name)]
IntIdAnnotation = Annotated[int, AfterValidator(validators.positive_number)]
RoleCodeAnnotation = Annotated[int, AfterValidator(validators.not_negative_number)]
DescriptionAnnotation = Annotated[str, AfterValidator(validators.description_string)]
StrIntIdAnnotation = Annotated[str, AfterValidator(validators.string_positive_number)]
