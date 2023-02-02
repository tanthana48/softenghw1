import yaml
from flask import Flask
from flask_mysqldb import MySQL

from src.vending import vending_machine

mysql = MySQL()


def create_app() -> Flask:
    """Create flask app."""
    app = Flask(__name__)

    app.register_blueprint(vending_machine.machine_blueprint)

    app.config["SECRET_KEY"] = "Never push this line to github public repo"

    cred = yaml.load(open("cred.yaml"), Loader=yaml.Loader)
    app.config["MYSQL_HOST"] = cred["mysql_host"]
    app.config["MYSQL_USER"] = cred["mysql_user"]
    app.config["MYSQL_PASSWORD"] = cred["mysql_password"]
    app.config["MYSQL_DB"] = cred["mysql_db"]
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
