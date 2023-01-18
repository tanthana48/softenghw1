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
    queryStatement = f"SELECT * FROM vendingmachine"
    print(queryStatement)
    result_value = cur.execute(queryStatement) 
    if result_value > 0:
        machines = jsonify(cur.fetchall())
    else:
        machines = jsonify(None)
    mysql.connection.commit()
    cur.close()
    return machines

@app.route("/create-machine", methods=['POST'])
def createMachine():
    if request.method == 'POST':
        name = request.args.get("name")
        location = request.args.get("location")
        print(name)
        print(location)
        if name == None or location == None:
            return "Plese put both name and location"
        cur = mysql.connection.cursor()
        queryStatement = f"INSERT INTO vendingmachine(machine_name, location, product) values ('{name}', '{location}', json_object())"
        print(queryStatement)
        cur.execute(queryStatement) 
        mysql.connection.commit()
        cur.close()
        return "Sucessfully Created"
    else:
        return None

@app.route('/delete-machine/<int:id>/', methods=['GET'])
def deleteMachine(id):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        queryStatement = f"DELETE FROM vendingmachine WHERE id = {id}"
        print(queryStatement)
        cur.execute(queryStatement)
        mysql.connection.commit()
        cur.close()
        return "Successfully Deleted"
    else:
        return None
    
@app.route("/add-product", methods=['POST'])
def addProduct():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        id = request.args.get("machineid")
        productName = request.args.get("name")
        amount = request.args.get("amount")
        if productName == None or amount == None or id == None:
            return "Plese put machineid, product and amount"
        checkIdStatement = f"Select id from vendingmachine where id = {id}"
        result_value = cur.execute(checkIdStatement)
        #check whether there is this machine id or not 
        if result_value > 0:
            checkProductStatement = f"Select json_extract(product, '$.{productName}') from vendingmachine where id = {id} and JSON_EXTRACT(product, '$.{productName}') IS NOT NULL"
            productresult = cur.execute(checkProductStatement)
            #checkwhether there is this product or not
            if productresult > 0:
                return "This product is already on the machine"
            else:
                addStatement = f"update vendingmachine set product = json_insert(product, '$.{productName}', '{amount}') where id = {id}"
                cur.execute(addStatement)
        else:
            return "Dont have this machine id"
        print(productName)
        print(amount)
        mysql.connection.commit()
        cur.close()
        return "Sucessfully Added"
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)