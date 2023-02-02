import sys

import pytest
import yaml
from flask import Flask

sys.path.append(".")
from app import mysql  # noqa: E402
from src.vending import vending_machine  # noqa: E402


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(vending_machine.machine_blueprint)
    client = app.test_client()

    cred = yaml.load(open("cred.yaml"), Loader=yaml.Loader)
    app.config["MYSQL_HOST"] = cred["mysql_host"]
    app.config["MYSQL_USER"] = cred["mysql_user"]
    app.config["MYSQL_PASSWORD"] = cred["mysql_password"]
    app.config["MYSQL_DB"] = cred["mysql_db"]
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    mysql.init_app(app)

    yield client
