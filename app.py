from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = "Never push this line to github public repo"

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = cred['mysql_host']
app.config['MYSQL_USER'] = cred['mysql_user']
app.config['MYSQL_PASSWORD'] = cred['mysql_password']
app.config['MYSQL_DB'] = cred['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


def select_query(query_statement: str):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute(query_statement)
            result = cur.fetchall()
            return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e))


def action_query(query_statement: str):
    try:
        with mysql.connection.cursor() as cur:
            cur.execute(query_statement)
            mysql.connection.commit()
            return jsonify(message="Success")
    except Exception as e:
        return jsonify(error=str(e))


@app.route("/machine")
def machine_list():
    query_statement = f"SELECT * FROM vendingmachine"
    return select_query(query_statement)


@app.route('/product-list/<int:machine_id>/')
def product_list(machine_id):
    query_statement = f"SELECT * FROM product where machine_id = {machine_id}"
    return select_query(query_statement)


@app.route("/create-machine", methods=['POST'])
def create_machine():
    args = request.args
    name = args.get("name")
    location = args.get("location")
    query_statement = f"INSERT INTO vendingmachine(machine_name, location) values ('{name}', '{location}')"
    return action_query(query_statement)


@app.route("/edit-machine", methods=['POST'])
def edit_machine():
    args = request.args
    machine_id = args.get("id")
    name = args.get("name")
    query_statement = f"update vendingmachine set machine_name = {name} where id = '{machine_id}'"
    return action_query(query_statement)


@app.route('/delete-machine/<int:id>/', methods=['GET'])
def delete_machine(id):
    query_statement = f"DELETE FROM vendingmachine WHERE id = {id}"
    return action_query(query_statement)


@app.route("/add-product", methods=['POST'])
def add_product():
    args = request.args
    machine_id = args.get("machine_id")
    product_name = args.get("product_name")
    amount = args.get("amount")
    query_statement = f"INSERT INTO product(machine_id, product_name, amount) values ('{machine_id}', '{product_name}', '{amount}')"
    return action_query(query_statement)


@app.route("/edit-product", methods=['POST'])
def edit_product():
    args = request.args
    product_id = args.get("product_id")
    amount = args.get("amount")
    query_statement = f"UPDATE product set amount = {amount} where product_id = {product_id}"
    return action_query(query_statement)


@app.route("/remove-product/<int:product_id>/", methods=['POST'])
def remove_product(product_id):
    query_statement = f"DELETE FROM product WHERE product_id = {product_id}"
    return action_query(query_statement)


if __name__ == '__main__':
    app.run(debug=True)
