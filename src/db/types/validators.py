import re
from pydantic import AfterValidator


def _is_email(email: str) -> str:
    pattern = r"^[a-zA-Z0-9_\.]+@[a-zA-Z0-9_\.]+\.[a-z]{2,5}"
    assert re.fullmatch(pattern, email) is not None, f"String {email} is not a valid email"
    return email
is_email = AfterValidator(_is_email)
