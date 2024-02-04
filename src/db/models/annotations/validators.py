"""Validating functions for the application"""
import re


def email_string(email: str) -> str:
    """Check if given string is email

    Args:
        email: string to check
    Returns:
        email
    Raises:
        ValueError: If string is not a valid email
    """
    pattern = (r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:"
               r"[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e"
               r"-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a"
               r"-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2("
               r"5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08"
               r"\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
    match = re.match(pattern, email) is not None
    if not match:
        raise ValueError(f"String {email} is not a valid email")
    return email


def positive_number(number: int) -> int:
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


def domain_name(domain: str) -> str:
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


def name_string(name: str) -> str:
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


def description_string(description: str) -> str:
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


def not_negative_number(number: int) -> int:
    """
    Check if given number is not negative
    Args:
        number: number to check
    Returns:
        number
    Raises:
        ValueError: is number is negative
    """

    if number < 0:
        raise ValueError(f"Number {number} must be a positive number")
    return number


def string_id(string: str) -> str:
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
