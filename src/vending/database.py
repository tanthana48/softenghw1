from typing import Dict

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Machine(db.Model):
    """Machine object.

    machine_id: machine id (primary key)
    name: machine name
    location: Location
    """

    machine_id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def to_json(self) -> Dict[str, str]:
        """Return machine info to json."""
        return {"machine_id": self.machine_id, "machine_name": self.machine_name, "location": self.location}


class Product(db.Model):
    """Product object.

    product_id: product id (primary key)
    machine_id: machine id (foreign key)
    product_name: product_name
    amount: amount of product
    """

    product_id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.machine_id"), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def to_json(self) -> Dict[str, str]:
        """Return machine info to json."""
        return {
            "product_id": self.product_id,
            "machine_id": self.machine_id,
            "product_name": self.product_name,
            "amount": self.amount,
        }
