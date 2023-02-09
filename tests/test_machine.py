from flask.testing import FlaskClient

from vending.vending_machine import status


def test_status():
    assert status(0) == {"message": "Success"}
    assert status(1) == {"error": "Missing required data"}
    assert status(2) == {"error": "Machine not found"}
    assert status(3) == {"error": "Product not found"}


def test_machine_list(client: FlaskClient):
    response = client.get("/machine")
    assert response.status_code == 200


def test_product_list(client: FlaskClient):
    response = client.get("/product-list/1/")
    assert response.status_code == 200


create_machine: str = "/create-machine"


def test_create_machine(client: FlaskClient):
    response = client.post(create_machine, data={"name": "Test Machine", "location": "Test Location"})
    assert response.status_code == 200
    assert response.get_json() == status(0)


def test_create_machine_fail(client: FlaskClient):
    response = client.post(create_machine, data={"location": "Test Location"})
    assert response.get_json() == status(1)


def test_create_machine2(client: FlaskClient):
    response = client.post(create_machine, data={"name": "Test Machine2", "location": "Test Location2"})
    assert response.status_code == 200
    assert response.get_json() == status(0)


edit_machine: str = "/edit-machine"


def test_edit_machine(client: FlaskClient):
    response = client.post(edit_machine, data={"machine_id": 1, "name": "Test", "location": "Test"})
    assert response.status_code == 200
    assert response.get_json() == status(0)


def test_edit_machine_fail(client: FlaskClient):
    response = client.post(edit_machine, data={"name": "Test", "location": "Test"})
    assert response.get_json() == status(1)


def test_edit_machine_fail2(client: FlaskClient):
    response = client.post(edit_machine, data={"machine_id": 100, "name": "Test", "location": "Test"})
    assert response.get_json() == status(2)


def test_delete_machine(client: FlaskClient):
    response = client.get("/delete-machine/1/")
    assert response.status_code == 200
    assert response.get_json() == status(0)


def test_delete_machine_fail(client: FlaskClient):
    response = client.get("/delete-machine/100/")
    assert response.get_json() == status(2)


def test_add_product(client: FlaskClient):
    response = client.post("/add-product", data={"machine_id": 2, "product_name": "Test Product", "amount": 10})
    assert response.status_code == 200
    assert response.get_json() == status(0)


def test_add_product2(client: FlaskClient):
    response = client.post("/add-product", data={"machine_id": 2, "product_name": "Test", "amount": 10})
    assert response.status_code == 200
    assert response.get_json() == status(0)


def test_edit_product(client: FlaskClient):
    response = client.post("/edit-product", data={"product_id": 1, "amount": 100})
    assert response.status_code == 200
    assert response.get_json() == status(0)


def test_edit_product_fail(client: FlaskClient):
    response = client.post("/edit-product", data={"product_id": 100, "amount": 100})
    assert response.get_json() == status(3)


def test_remove_product(client: FlaskClient):
    response = client.get("/delete-product/2/")
    assert response.status_code == 200
    assert response.get_json() == status(0)


def test_remove_product_fail(client: FlaskClient):
    response = client.get("/delete-product/200/")
    assert response.get_json() == status(3)
