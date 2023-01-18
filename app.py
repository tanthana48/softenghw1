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

@app.route("/createmachine", methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)