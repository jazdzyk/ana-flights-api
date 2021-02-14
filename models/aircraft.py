from db import db
from models import BaseModel


class AircraftModel(db.Model, BaseModel):
    __tablename__ = "aircrafts"

    brand = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)

    flights = db.relationship("FlightModel", foreign_keys="FlightModel.aircraft_id", lazy="dynamic")
