"""Regex validators for the application"""
import re


def validate_email(email: str) -> bool:
    """Check if given string is email

    Args:
        email (str): string to check

    Returns:
        bool: True if string is email, else False
    """
    pattern = r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'
    return re.match(pattern, email) is not None
