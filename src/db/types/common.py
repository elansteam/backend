"""Common project types"""
import re
from typing import Annotated
from pydantic import AfterValidator



def _is_email(email: str) -> str:
    """Check if given string is email

    Args:
        email: string to check
    Returns:
        email
    Raises:
        ValueError: If string is not a valid email
    """
    pattern = r"^[a-zA-Z0-9_\.]+@[a-zA-Z0-9_\.]+\.[a-z]{2,5}"
    if re.fullmatch(pattern, email) is None:
        raise ValueError(f"String {email} is not a valid email")
    return email
Email = Annotated[str, AfterValidator(_is_email)]

def _is_positive_number(number: int) -> int:
    """Check if given integer is positive
    Args:
        number: number to check
    Returns:
        number
    Raises:
        ValueError: If number not positive
    """

    if number <= 0:
        raise ValueError(f"Number {number} must be a positive number")
    return number
IntegerId = Annotated[int, AfterValidator(_is_positive_number)]

def _is_domain_name(domain: str) -> str:
    """
    Check if given domain is valid domain
    Args:
        domain: domain to check
    Returns:
        Domain
    Raises:
        ValueError: If domain is not valid
    """
    return domain  # TODO: define behaviour
DomainName = Annotated[str, AfterValidator(_is_domain_name)]

def _is_object_name(name: str) -> str:
    """
    Check if given name is valid name
    Args:
        name: name to check
    Returns:
        name
    Raises:
        ValueError: is name is not valid
    """
    return name  # TODO: define behaviour
ObjectName = Annotated[str, AfterValidator(_is_object_name)]

def _is_object_description(description: str) -> str:
    """
    Check if given description is valid description
    Args:
        description: description to check
    Returns:
        description
    Raises:
        ValueError: is description is not valid
    """
    return description  # TODO: define behaviour
ObjectDescription = Annotated[str, AfterValidator(_is_object_description)]

def _is_role_code(number: int) -> int:
    if number < 0:
        raise ValueError("Role code can not be negative")
    return number
RoleCode = Annotated[int, AfterValidator(_is_role_code)]

def _string_id(string: str) -> str:
    """
    Check if given string is valid id
    Args:
        string: string to validate
    Returns:
        string
    Raises:
        ValueError: is string is not valid
    """
    pattern = r"[a-z]+(?:_[a-z]+)*"
    if re.fullmatch(pattern, string) is None:
        raise ValueError("String is not valid")
    return string
StringId = Annotated[str, AfterValidator(_string_id)]
