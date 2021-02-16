from typing import List

from db import db
from models import BaseModel


class AircraftModel(db.Model, BaseModel):
    __tablename__ = "aircrafts"

    brand = db.Column(db.String(30), nullable=False, unique=True)
    model = db.Column(db.String(30), nullable=False)

    flights = db.relationship("FlightModel", foreign_keys="FlightModel.aircraft_id", lazy="dynamic")

    def __init__(self, brand, model):
        BaseModel.__init__(self)
        self.brand = brand
        self.model = model

    @classmethod
    def find_by_brand(cls, brand: str) -> List["AircraftModel"]:
        return cls.query.filter_by(brand=brand).all()

    @classmethod
    def find_by_brand_and_model(cls, brand: str, model: str) -> "AircraftModel":
        return cls.query.filter_by(brand=brand, model=model).first()
