import pytest
from flask.testing import FlaskClient


@pytest.fixture
def test_create_machine(client: FlaskClient):
    data = {"name": "test", "location": "test"}

    r = client.post("/create-machine", data)

    assert r.json() == {"message": "Success"}


def test_edit_machine(client: FlaskClient):
    url = "http://127.0.0.1:5000/edit-machine"

    data = {"machine_id": "1", "name": "test2"}

    r = client.post(url, data=data)

    assert r.json() == {"message": "Success"}


def test_delete_machine(client: FlaskClient):
    url = "http://127.0.0.1:5000/delete-machine/5"

    r = client.get(url)

    assert r.json() == {"message": "Success"}


def test_add_product(client: FlaskClient):
    url = "http://127.0.0.1:5000/add-product"

    data = {"machine_id": "2", "product_name": "sprite", "amount": "10"}

    r = client.post(url, data=data)

    assert r.json() == {"message": "Success"}


def test_edit_product(client: FlaskClient):
    url = "http://127.0.0.1:5000/edit-product"

    data = {"product_id": "1", "amount": "10"}

    r = client.post(url, data=data)

    assert r.json() == {"message": "Success"}


def test_remove_product(client: FlaskClient):
    url = "http://127.0.0.1:5000/remove-product/1"

    r = client.get(url)

    assert r.json() == {"message": "Success"}
