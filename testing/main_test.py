"""
Main project tests
"""
import pytest


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Base fixture, that setting up database and start fastapi client"""
    print("Setting up")
    yield
    print("Teardown")
