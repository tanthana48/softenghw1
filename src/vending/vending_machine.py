from typing import Union

from database import Machine, Product, db
from flask import Blueprint, Response, jsonify, request

machine_blueprint = Blueprint("vending_machine", __name__)


@machine_blueprint.route("/machine")
def machine_list() -> Union[Response, dict[str, str]]:
    """List all machine info."""
    machines = Machine.query.all()
    return jsonify([m.to_json() for m in machines])


@machine_blueprint.route("/product-list/<int:machine_id>/")
def product_list(machine_id: int) -> Union[Response, dict[str, str]]:
    """List all product info by machine id."""
    products = Product.query.filter_by(machine_id=machine_id).all()
    return jsonify([p.to_json() for p in products])


@machine_blueprint.route("/create-machine", methods=["POST"])
def create_machine() -> dict[str, str]:
    """Create new machine."""
    form = request.form
    name = form.get("name")
    location = form.get("location")

    if not name or not location:
        return {"error": "Missing required data"}

    machine = Machine(machine_name=name, location=location)
    db.session.add(machine)
    db.session.commit()
    return {"message": "Success"}
