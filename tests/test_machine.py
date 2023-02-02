from flask import Flask, jsonify
from flask.testing import FlaskClient

from src.vending.vending_machine import action_query, select_query


def test_select_query(client: FlaskClient, app: Flask):
    """Test select_query."""
    with app.app_context():
        result = select_query("SELECT * FROM machine")
        client_request = client.get("/machine")
        assert result == client_request


def test_action_query(client: FlaskClient, app: Flask):
    with app.app_context():
        result = action_query("INSERT INTO machine(machine_name, location) values ('test', 'somewhere')")
        assert result == jsonify(message="Success")


def test_create_machine(client: FlaskClient):
    data = {"name": "test", "location": "test"}

    r = client.post("/create-machine", data=data).json

    assert r == {"message": "Success"}


def test_edit_machine(client: FlaskClient):
    data = {"id": "1", "name": "test222", "location": "tdadadada"}

    r = client.post("/edit-machine", data=data).json

    assert r == {"message": "Success"}


def test_delete_machine(client: FlaskClient):
    r = client.get("/delete-machine/7").json

    assert r == {"message": "Success"}


def test_add_product(client: FlaskClient):
    data = {"machine_id": "2", "product_name": "sprite", "amount": "10"}

    r = client.post("/add-product", data=data)

    assert r.json() == {"message": "Success"}


def test_edit_product(client: FlaskClient):
    data = {"product_id": "1", "amount": "10"}

    r = client.post("/edit-product", data=data)

    assert r.json() == {"message": "Success"}


def test_remove_product(client: FlaskClient):
    r = client.get("/remove-product/1")

    assert r.json() == {"message": "Success"}
