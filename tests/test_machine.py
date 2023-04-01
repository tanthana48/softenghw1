from flask.testing import FlaskClient

from vending.app import create_app
from vending.database import Machine, Product, StockTimeline, db
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


def test_create_and_add_product():
    app = create_app()

    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        product = Product(machine_id=machine.machine_id, product_name="Test Product", amount=10)
        db.session.add(product)
        db.session.commit()

        assert product.product_id is not None


def test_create_and_add_stocktimeline():
    app = create_app()

    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        product = Product(machine_id=machine.machine_id, product_name="Test Product", amount=10)
        db.session.add(product)
        db.session.commit()

        stocktimeline = StockTimeline(machine_id=machine.machine_id, product_id=product.product_id, amount=10)
        db.session.add(stocktimeline)
        db.session.commit()

        assert stocktimeline.id is not None


def test_machine_to_json():
    app = create_app()

    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        machine_json = machine.to_json()

        assert machine_json["machine_id"] == machine.machine_id
        assert machine_json["machine_name"] == "Test Machine"
        assert machine_json["location"] == "Test Location"


def test_product_to_json():
    app = create_app()

    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        product = Product(machine_id=machine.machine_id, product_name="Test Product", amount=10)
        db.session.add(product)
        db.session.commit()

        product_json = product.to_json()

        assert product_json["product_id"] == product.product_id
        assert product_json["machine_id"] == machine.machine_id
        assert product_json["product_name"] == "Test Product"
        assert product_json["amount"] == 10


def test_stock_timeline_to_json():
    app = create_app()

    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        product = Product(machine_id=machine.machine_id, product_name="Test Product", amount=10)
        db.session.add(product)
        db.session.commit()

        stock_timeline = StockTimeline(machine_id=machine.machine_id, product_id=product.product_id, amount=10)
        db.session.add(stock_timeline)
        db.session.commit()

        stock_timeline_json = stock_timeline.to_json()

        assert stock_timeline_json["id"] == stock_timeline.id
        assert stock_timeline_json["machine_id"] == machine.machine_id
        assert stock_timeline_json["machine_name"] == "Test Machine"
        assert stock_timeline_json["product_id"] == product.product_id
        assert stock_timeline_json["product_name"] == "Test Product"
        assert stock_timeline_json["amount"] == 10


def test_status_function():
    assert status(0) == {"message": "Success"}
    assert status(1) == {"error": "Missing required data"}
    assert status(2) == {"error": "Machine not found"}
    assert status(3) == {"error": "Product not found"}


def test_edit_machine_app(app: create_app, client: FlaskClient):
    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        response = client.post(
            "/edit-machine", data={"machine_id": machine.machine_id, "name": "New Name", "location": "New Location"}
        )
        assert response.json == status(0)

        edited_machine = Machine.query.get(machine.machine_id)
        assert edited_machine.machine_name == "New Name"
        assert edited_machine.location == "New Location"


def test_add_product_app(app: create_app, client: FlaskClient):
    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        response = client.post(
            "/add-product", data={"machine_id": machine.machine_id, "product_name": "Test Product", "amount": 10}
        )
        assert response.json == status(0)

        product = Product.query.filter_by(machine_id=machine.machine_id).first()
        assert product is not None
        assert product.product_name == "Test Product"
        assert product.amount == 10


def test_edit_product_app(app: create_app, client: FlaskClient):
    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        product = Product(machine_id=machine.machine_id, product_name="Test Product", amount=10)
        db.session.add(product)
        db.session.commit()

        response = client.post(
            "/edit-product",
            data={
                "product_id": product.product_id,
                "machine_id": machine.machine_id,
                "product_name": "New Product",
                "amount": 20,
            },
        )
        assert response.json == status(0)

        edited_product = Product.query.get(product.product_id)
        assert edited_product.product_name == "New Product"
        assert edited_product.amount == 20


def test_get_stock_timeline_app(app: create_app, client: FlaskClient):
    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        product = Product(machine_id=machine.machine_id, product_name="Test Product", amount=10)
        db.session.add(product)
        db.session.commit()

        stock_timeline = StockTimeline(machine_id=machine.machine_id, product_id=product.product_id, amount=10)
        db.session.add(stock_timeline)
        db.session.commit()

        response = client.get(f"/stock-timeline/{machine.machine_id}/{product.product_id}")
        assert response.status_code == 200
        assert len(response.json) == 1


def test_get_product_timeline_app(app: create_app, client: FlaskClient):
    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        product = Product(machine_id=machine.machine_id, product_name="Test Product", amount=10)
        db.session.add(product)
        db.session.commit()

        stock_timeline = StockTimeline(machine_id=machine.machine_id, product_id=product.product_id, amount=10)
        db.session.add(stock_timeline)
        db.session.commit()

        response = client.get(f"/product-timeline/{product.product_id}")
        assert response.status_code == 200
        assert len(response.json) == 1


def test_get_machine_timeline_app(app: create_app, client: FlaskClient):
    with app.app_context():
        machine = Machine(machine_name="Test Machine", location="Test Location")
        db.session.add(machine)
        db.session.commit()

        product = Product(machine_id=machine.machine_id, product_name="Test Product", amount=10)
        db.session.add(product)
        db.session.commit()

        stock_timeline = StockTimeline(machine_id=machine.machine_id, product_id=product.product_id, amount=10)
        db.session.add(stock_timeline)
        db.session.commit()

        response = client.get(f"/machine-timeline/{machine.machine_id}")
        assert response.status_code == 200
        assert len(response.json) == 1
