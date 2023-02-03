from database import db
from flask import Flask
from vending_machine import machine_blueprint


def create_app() -> Flask:
    """Create flask app."""
    app = Flask(__name__)
    app.register_blueprint(machine_blueprint)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:mysecretpassword@localhost:5432/vending_machine"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
