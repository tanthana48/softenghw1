import os

from dotenv import load_dotenv
from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()


def create_app() -> Flask:
    """Create flask app."""
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "Never push this line to github public repo"

    load_dotenv()
    app.config["MYSQL_HOST"] = os.getenv("DB_HOST")
    app.config["MYSQL_USER"] = os.getenv("DB_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("DB_PASS")
    app.config["MYSQL_DB"] = "vending_machine"
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"

    mysql.init_app(app)

    with app.app_context():
        from src.vending import vending_machine

        app.register_blueprint(vending_machine.machine_blueprint)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
