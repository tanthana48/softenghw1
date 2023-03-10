import pytest
from flask import Flask
from flask.testing import FlaskClient

from vending.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"WTF_CSRF_ENABLED": False})

    yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()
