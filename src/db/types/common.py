import re
from typing import Annotated
from pydantic import AfterValidator



def _is_email(email: str) -> str:
    pattern = r"^[a-zA-Z0-9_\.]+@[a-zA-Z0-9_\.]+\.[a-z]{2,5}"
    assert re.fullmatch(pattern, email) is not None, f"String {email} is not a valid email"
    return email
Email = Annotated[str, AfterValidator(_is_email)]

def _is_positive_number(number: int) -> int:
    assert number > 0, f"Number {number} must be a positive number"
    return number
IntegerId = Annotated[int, AfterValidator(_is_positive_number)]

def _is_domain_name(domain: str) -> str:
    return domain  # TODO: define behaviour
DomainName = Annotated[str, AfterValidator(_is_domain_name)]

def _is_object_name(name: str) -> str:
    return name  # TODO: define behaviour
ObjectName = Annotated[str, AfterValidator(_is_object_name)]

def _is_object_description(description: str) -> str:
    return description  # TODO: define behaviour
ObjectDescription = Annotated[str, AfterValidator(_is_object_description)]

def _is_role_code(number: int) -> int:
    assert number >= 0, "Role code can not be negative"
    return number
RoleCode = Annotated[int, AfterValidator(_is_role_code)]

def _string_id(string: str) -> str:
    pattern = r"[a-z]+(?:_[a-z]+)*"
    assert re.fullmatch(pattern, string) is not None, "String id is not valid"
    return string
StringId = Annotated[str, AfterValidator(_string_id)]
