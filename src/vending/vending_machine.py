from typing import Dict

from flask import Blueprint, Response, jsonify, request

machine_blueprint = Blueprint("vending_machine", __name__)


def select_query(query_statement: str) -> Dict[str, str]:
    """Execute query and result in json."""
    try:
        from app import mysql

        with mysql.connection.cursor() as cur:
            cur.execute(query_statement)
            result = cur.fetchall()
            return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e))


def action_query(query_statement: str) -> Dict[str, str]:
    """Execute query and result in json."""
    try:
        from app import mysql

        with mysql.connection.cursor() as cur:
            cur.execute(query_statement)
            mysql.connection.commit()
            return jsonify(message="Success")
    except Exception as e:
        return jsonify(error=str(e))


@machine_blueprint.route("/machine")
def machine_list() -> Response:
    """List all machine info."""
    query_statement = "SELECT * FROM machine"
    return select_query(query_statement)


@machine_blueprint.route("/product-list/<int:machine_id>/")
def product_list(machine_id: int) -> Response:
    """List all product info by machine id."""
    query_statement = f"SELECT * FROM product where machine_id = {machine_id}"
    return select_query(query_statement)


@machine_blueprint.route("/create-machine", methods=["POST"])
def create_machine() -> dict[str, str]:
    """Create new machine."""
    args = request.args
    name = args.get("name")
    location = args.get("location")
    query_statement = f"INSERT INTO machine(machine_name, location) values ('{name}', '{location}')"
    return action_query(query_statement)


@machine_blueprint.route("/edit-machine", methods=["POST"])
def edit_machine() -> dict[str, str]:
    """Edit machine."""
    args = request.args
    machine_id = args.get("id")
    name = args.get("name")
    location = args.get("location")
    query_statement = (
        f"UPDATE machine set machine_name = IFNULL('{name}', machine_name)"
        f", location = IFNULL('{location}', location) where id = {machine_id}"
    )
    return action_query(query_statement)


@machine_blueprint.route("/delete-machine/<int:id>/", methods=["GET"])
def delete_machine(id: int) -> dict[str, str]:
    """Delete machine by id."""
    query_statement = f"DELETE FROM machine WHERE id = {id}"
    return action_query(query_statement)


@machine_blueprint.route("/add-product", methods=["POST"])
def add_product() -> dict[str, str]:
    """Add product."""
    args = request.args
    machine_id = args.get("machine_id")
    product_name = args.get("product_name")
    amount = args.get("amount")
    query_statement = (
        f"INSERT INTO product(machine_id, product_name, amount) values ('{machine_id}', '{product_name}', '{amount}')"
    )
    return action_query(query_statement)


@machine_blueprint.route("/edit-product", methods=["POST"])
def edit_product() -> dict[str, str]:
    """Edit product."""
    args = request.args
    product_id = args.get("product_id")
    amount = args.get("amount")
    query_statement = f"UPDATE product set amount = IFNULL({amount}, amount) where product_id = {product_id}"
    return action_query(query_statement)


@machine_blueprint.route("/remove-product/<int:product_id>/")
def remove_product(product_id: int) -> dict[str, str]:
    """Remove product by id."""
    query_statement = f"DELETE FROM product WHERE product_id = {product_id}"
    return action_query(query_statement)
