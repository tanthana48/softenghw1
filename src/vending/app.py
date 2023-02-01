import yaml
from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()


def create_app() -> Flask:
    """Create flask app."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Never push this line to github public repo"

    cred = yaml.load(open("cred.yaml"), Loader=yaml.Loader)
    app.config["MYSQL_HOST"] = cred["mysql_host"]
    app.config["MYSQL_USER"] = cred["mysql_user"]
    app.config["MYSQL_PASSWORD"] = cred["mysql_password"]
    app.config["MYSQL_DB"] = cred["mysql_db"]
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    with app.app_context():
        from machine import machine

        app.register_blueprint(machine)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
