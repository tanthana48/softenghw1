from datetime import datetime
from typing import Dict

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class StockTimeline(db.Model):
    """Stock timeline object.

    id: timeline id (primary key)
    machine_id: machine id (foreign key)
    product_id: product id (foreign key)
    date_time: date and time of the stock update
    amount: amount of product
    """

    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey("machine.machine_id", ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id", ondelete="CASCADE"), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    machine = db.relationship("Machine", backref=db.backref("machine_timeline", lazy=True), cascade="all,delete-orphan")
    product = db.relationship("Product", backref=db.backref("product_timeline", lazy=True), cascade="all,delete")

    def to_json(self) -> Dict[str, str]:
        """Return stock timeline info to json."""
        return {
            "id": self.id,
            "machine_id": self.machine_id,
            "machine_name": self.machine.machine_name,
            "product_id": self.product_id,
            "product_name": self.product.product_name,
            "date_time": self.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "amount": self.amount,
        }


class Machine(db.Model):
    """Machine object.

    machine_id: machine id (primary key)
    name: machine name
    location: Location
    """

    machine_id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    machine_products = db.relationship(
        "Product", backref=db.backref("machine_products", lazy=True), cascade="all, delete"
    )

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

    stock_timelines = db.relationship("StockTimeline", backref=db.backref("products", lazy=True), cascade="all, delete")
    machine = db.relationship("Machine")

    def to_json(self) -> Dict[str, str]:
        """Return machine info to json."""
        return {
            "product_id": self.product_id,
            "machine_id": self.machine_id,
            "product_name": self.product_name,
            "amount": self.amount,
        }

    def add_or_update_product(self):
        """Add or update product and update stock_timeline."""
        db.session.add(self)
        db.session.commit()

        db.session.flush()  # flush the session to ensure that the product_id is available

        stock_timeline = StockTimeline(
            machine_id=self.machine_id, product_id=self.product_id, date_time=datetime.utcnow(), amount=self.amount
        )

        db.session.add(stock_timeline)
        db.session.commit()
