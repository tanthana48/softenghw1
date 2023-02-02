import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app


@pytest.fixture
def app() -> Flask:
    """Create new app for each test."""
    return create_app()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create new test_client."""
    return app.test_client()
