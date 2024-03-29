from typing import Union

from flask import Blueprint, Response, jsonify, request

from vending.database import Machine, Product, StockTimeline, db

machine_blueprint = Blueprint("vending_machine", __name__)


def status(code: int) -> dict[str, str]:
    """Return the status."""
    if code == 3:
        return {"error": "Product not found"}
    elif code == 2:
        return {"error": "Machine not found"}
    elif code == 1:
        return {"error": "Missing required data"}
    elif code == 0:
        return {"message": "Success"}


@machine_blueprint.route("/machine")
def machine_list() -> Union[Response, dict[str, str]]:
    """List all machine info."""
    machines = Machine.query.all()
    return jsonify([m.to_json() for m in machines])


@machine_blueprint.route("/create-machine", methods=["POST"])
def create_machine() -> dict[str, str]:
    """Create new machine."""
    form = request.form
    name = form.get("name")
    location = form.get("location")

    if not name or not location:
        return status(1)

    machine = Machine(machine_name=name, location=location)
    db.session.add(machine)
    db.session.commit()
    return status(0)


@machine_blueprint.route("/edit-machine", methods=["POST"])
def edit_machine() -> dict[str, str]:
    """Edit machine."""
    form = request.form
    machine_id = form.get("machine_id")
    name = form.get("name")
    location = form.get("location")

    if not machine_id:
        return status(1)

    machine = Machine.query.filter_by(machine_id=machine_id).first()
    if not machine:
        return status(2)

    if name:
        machine.machine_name = name
    if location:
        machine.location = location

    db.session.commit()
    return status(0)


@machine_blueprint.route("/delete-machine/<int:machine_id>/")
def delete_machine(machine_id: int) -> dict[str, str]:
    """Delete machine by id."""
    machine = Machine.query.filter_by(machine_id=machine_id).first()
    if not machine:
        return status(2)
    db.session.delete(machine)
    db.session.commit()
    return status(0)


@machine_blueprint.route("/product-list/<int:machine_id>/")
def product_list(machine_id: int) -> Union[Response, dict[str, str]]:
    """List all product info by machine id."""
    products = Product.query.filter_by(machine_id=machine_id).all()
    return jsonify([p.to_json() for p in products])


@machine_blueprint.route("/add-product", methods=["POST"])
def add_product() -> dict[str, str]:
    """Add product."""
    form = request.form
    machine_id = form.get("machine_id")
    product_name = form.get("product_name")
    amount = form.get("amount")

    if not machine_id or not product_name or not amount:
        return status(1)

    product = Product(machine_id=machine_id, product_name=product_name, amount=amount)
    product.add_or_update_product()
    db.session.add(product)
    db.session.commit()
    return status(0)


@machine_blueprint.route("/edit-product", methods=["POST"])
def edit_product() -> dict[str, str]:
    """Edit product."""
    form = request.form
    product_id = form.get("product_id")
    machine_id = form.get("machine_id")
    product_name = form.get("product_name")
    amount = form.get("amount")

    if not product_id:
        return status(1)

    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return status(3)
    if machine_id:
        product.machine_id = machine_id
    if product_name:
        product.product_name = product_name
    if amount:
        product.amount = amount
    product.add_or_update_product()
    db.session.commit()

    return status(0)


@machine_blueprint.route("/delete-product/<int:product_id>/")
def delete_product(product_id: int) -> dict[str, str]:
    """Delete product by id."""
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return status(3)

    db.session.delete(product)
    db.session.commit()

    return status(0)


@machine_blueprint.route("/stock-timeline/<int:machine_id>/<int:product_id>", methods=["GET"])
def get_stock_timeline(machine_id: int, product_id: int) -> Union[Response, dict[str, str]]:
    """Show stock timeline of specific product in specific machine."""
    timeline = StockTimeline.query.filter_by(machine_id=machine_id, product_id=product_id).all()
    return jsonify([t.to_json() for t in timeline])


@machine_blueprint.route("/product-timeline/<int:product_id>", methods=["GET"])
def get_product_timeline(product_id: int) -> Union[Response, dict[str, str]]:
    """Show stock timeline of specific product."""
    timeline = StockTimeline.query.filter_by(product_id=product_id).all()
    return jsonify([t.to_json() for t in timeline])


@machine_blueprint.route("/machine-timeline/<int:machine_id>", methods=["GET"])
def get_machine_timeline(machine_id: int) -> Union[Response, dict[str, str]]:
    """Show stock timeline of specific machine."""
    timeline = StockTimeline.query.filter_by(machine_id=machine_id).all()
    return jsonify([t.to_json() for t in timeline])
