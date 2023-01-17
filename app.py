from flask import Flask, request
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = cred['mysql_host']
app.config['MYSQL_USER'] = cred['mysql_user']
app.config['MYSQL_PASSWORD'] = cred['mysql_password']
app.config['MYSQL_DB'] = cred['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

def create_table():
    cursor = mysql.connection.cursor()
    mysql.connection.commit()
    cursor.close()
    return
@app.route("/list")
def list():
    
	return

if __name__ == '__main__':
	app.run(debug=True)