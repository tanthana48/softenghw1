from flask import Flask
from flask_wtf.csrf import CSRFProtect

from vending.database import db
from vending.vending_machine import machine_blueprint


def create_app() -> Flask:
    """Create flask app."""
    app = Flask(__name__)
    app.secret_key = "your_secret_key"
    app.register_blueprint(machine_blueprint)

    #csrf = CSRFProtect()
    #csrf.init_app(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:test@localhost:5432/vending_machine"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
