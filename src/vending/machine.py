from flask import Blueprint, Response, request
from query import action_query, select_query

machine = Blueprint("machine", __name__)


@machine.route("/machine")
def machine_list() -> Response:
    """List all machine info."""
    query_statement = "SELECT * FROM vendingmachine"
    return select_query(query_statement)


@machine.route("/product-list/<int:machine_id>/")
def product_list(machine_id: int) -> Response:
    """List all product info by machine id."""
    query_statement = f"SELECT * FROM product where machine_id = {machine_id}"
    return select_query(query_statement)


@machine.route("/create-machine", methods=["POST"])
def create_machine() -> Response:
    """Create new machine."""
    args = request.args
    name = args.get("name")
    location = args.get("location")
    query_statement = f"INSERT INTO vendingmachine(machine_name, location) values ('{name}', '{location}')"
    return action_query(query_statement)


@machine.route("/edit-machine", methods=["POST"])
def edit_machine() -> Response:
    """Edit machine."""
    args = request.args
    machine_id = args.get("id")
    name = args.get("name")
    query_statement = f"update vendingmachine set machine_name = {name} where id = '{machine_id}'"
    return action_query(query_statement)


@machine.route("/delete-machine/<int:id>/", methods=["GET"])
def delete_machine(id: int) -> Response:
    """Delete machine by id."""
    query_statement = f"DELETE FROM vendingmachine WHERE id = {id}"
    return action_query(query_statement)


@machine.route("/add-product", methods=["POST"])
def add_product() -> Response:
    """Add product."""
    args = request.args
    machine_id = args.get("machine_id")
    product_name = args.get("product_name")
    amount = args.get("amount")
    query_statement = (
        f"INSERT INTO product(machine_id, product_name, amount) values ('{machine_id}', '{product_name}', '{amount}')"
    )
    return action_query(query_statement)


@machine.route("/edit-product", methods=["POST"])
def edit_product() -> Response:
    """Edit product."""
    args = request.args
    product_id = args.get("product_id")
    amount = args.get("amount")
    query_statement = f"UPDATE product set amount = {amount} where product_id = {product_id}"
    return action_query(query_statement)


@machine.route("/remove-product/<int:product_id>/", methods=["POST"])
def remove_product(product_id: int) -> Response:
    """Remove product by id."""
    query_statement = f"DELETE FROM product WHERE product_id = {product_id}"
    return action_query(query_statement)
