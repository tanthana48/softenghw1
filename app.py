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


@app.route("/list")
def list():
    cur = mysql.connection.cursor()
    query_statement = f"SELECT * FROM vendingmachine"
    print(query_statement)
    result_value = cur.execute(query_statement)
    if result_value > 0:
        machines = jsonify(cur.fetchall())
    else:
        machines = jsonify(None)
    mysql.connection.commit()
    cur.close()
    return machines


@app.route("/create-machine", methods=['POST'])
def create_machine():
    try:
        if request.method == 'POST':
            name = request.args.get("name")
            location = request.args.get("location")
            print(name)
            print(location)
            if name == None or location == None:
                return "Please put both name and location"
            cur = mysql.connection.cursor()
            query_statement = f"INSERT INTO vendingmachine(machine_name, location) values ('{name}', '{location}')"
            print(query_statement)
            cur.execute(query_statement)
            mysql.connection.commit()
            cur.close()
            return jsonify(message='Successfully Created')
    except Exception as e:
        return jsonify(error=str(e))


@app.route('/delete-machine/<int:id>/', methods=['GET'])
def delete_machine(id):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        query_statement = f"DELETE FROM vendingmachine WHERE id = {id}"
        print(query_statement)
        result = cur.execute(query_statement)
        if result == 0:
            return "There is no this machine"
        mysql.connection.commit()
        cur.close()
        return "Successfully Deleted"
    else:
        return None


@app.route("/add-product", methods=['POST'])
def add_product():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        id = request.args.get("machineid")
        product_name = request.args.get("name")
        amount = request.args.get("amount")
        if product_name == None or amount == None or id == None:
            return "Plese put machineid, product and amount"
        check_id_statement = f"Select id from vendingmachine where id = {id}"
        result_value = cur.execute(check_id_statement)
        # check whether there is this machine id or not
        if result_value > 0:
            check_product_statement = f"Select json_extract(product, '$.{product_name}') from vendingmachine where id = {id} and JSON_EXTRACT(product, '$.{product_name}') IS NOT NULL"
            product_result = cur.execute(check_product_statement)
            # check whether there is this product or not
            if product_result > 0:
                return "This product is already on the machine"
            else:
                add_statement = f"update vendingmachine set product = json_insert(product, '$.{product_name}', '{amount}') where id = {id}"
                cur.execute(add_statement)
        else:
            return "Dont have this machine id"
        print(product_name)
        print(amount)
        mysql.connection.commit()
        cur.close()
        return "Sucessfully Added"
    else:
        return None


@app.route("/edit-product", methods=['POST'])
def edit_product():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        id = request.args.get("machineid")
        product_name = request.args.get("name")
        amount = request.args.get("amount")
        if product_name == None or amount == None or id == None:
            return "Plese put machineid, product and amount"
        check_id_statement = f"Select id from vendingmachine where id = {id}"
        result_value = cur.execute(check_id_statement)
        # check whether there is this machine id or not
        if result_value > 0:
            check_product_statement = f"Select json_extract(product, '$.{product_name}') from vendingmachine where id = {id} and JSON_EXTRACT(product, '$.{product_name}') IS NOT NULL"
            product_result = cur.execute(check_product_statement)
            # check whether there is this product or not
            if product_result > 0:
                add_statement = f"update vendingmachine set product = json_replace(product, '$.{product_name}', '{amount}') where id = {id}"
                cur.execute(add_statement)
            else:
                return "There is no this product in this machine"
        else:
            return "Dont have this machine id"
        print(product_name)
        print(amount)
        mysql.connection.commit()
        cur.close()
        return "Sucessfully Edited"
    else:
        return None


@app.route("/remove-product", methods=['POST'])
def remove_product():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        id = request.args.get("machineid")
        product_name = request.args.get("name")
        if product_name is None or id is None:
            return "Plese put both machineid and product"
        check_id_statement = f"Select id from vendingmachine where id = {id}"
        result_value = cur.execute(check_id_statement)
        # check whether there is this machine id or not
        if result_value > 0:
            check_product_statement = f"Select json_extract(product, '$.{product_name}') from vendingmachine where id = {id} and JSON_EXTRACT(product, '$.{product_name}') IS NOT NULL"
            product_result = cur.execute(check_product_statement)
            # check whether there is this product or not
            if product_result > 0:
                add_statement = f"update vendingmachine set product = json_remove(product, '$.{product_name}') where id = {id}"
                cur.execute(add_statement)
            else:
                return "There is no this product in this machine"
        else:
            return "Dont have this machine id"
        print(product_name)
        mysql.connection.commit()
        cur.close()
        return "Sucessfully Removed"
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)
