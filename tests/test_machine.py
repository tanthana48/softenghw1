from flask.testing import FlaskClient


def test_machine_list(client: FlaskClient):
    response = client.get("/machine")
    assert response.status_code == 200


def test_product_list(client: FlaskClient):
    response = client.get("/product-list/1/")
    assert response.status_code == 200


def test_create_machine(client: FlaskClient):
    response = client.post("/create-machine", data={"name": "Test Machine", "location": "Test Location"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Success"}


def test_create_machine2(client: FlaskClient):
    response = client.post("/create-machine", data={"name": "Test Machine2", "location": "Test Location2"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Success"}


def test_edit_machine(client: FlaskClient):
    response = client.post("/edit-machine", data={"machine_id": 1, "name": "Test", "location": "Test"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Success"}


def test_delete_machine(client: FlaskClient):
    response = client.get("/delete-machine/1/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Success"}


def test_add_product(client: FlaskClient):
    response = client.post("/add-product", data={"machine_id": 2, "product_name": "Test Product", "amount": 10})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Success"}


def test_add_product2(client: FlaskClient):
    response = client.post("/add-product", data={"machine_id": 2, "product_name": "Test", "amount": 10})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Success"}


def test_edit_product(client: FlaskClient):
    response = client.post("/edit-product", data={"product_id": 1, "amount": 100})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Success"}


def test_remove_product(client: FlaskClient):
    response = client.get("/delete-product/2/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Success"}
