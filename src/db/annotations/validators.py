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
    pattern = r"^[a-zA-Z0-9_\.]+@[a-zA-Z0-9_\.]+\.[a-z]{2,5}"
    if re.fullmatch(pattern, email) is None:
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


def string_positive_number(string: str) -> str:
    """
    Check if given string is a number and positive number
    Args:
        string: string to check
    Returns:
        string
    Raises:
        ValueError: if given string is not a positive number
    """
    num = 0
    try:
        num = int(string)
    except Exception as e:
        raise ValueError("string is not a number") from e
    if num <= 0:
        raise ValueError("String is not a positive number")
    return string
