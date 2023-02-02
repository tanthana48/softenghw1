import sys

import pytest
from flask import Flask
from flask.testing import FlaskClient

sys.path.append(".")
from app import create_app  # noqa: E402


@pytest.fixture()
def app():
    app = create_app()

    yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()
