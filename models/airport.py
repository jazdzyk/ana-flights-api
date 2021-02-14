from db import db
from models import BaseModel


class AirportModel(BaseModel):
    __tablename__ = "airports"

    name = db.Column(db.String(100), nullable=False)
    iata = db.Column(db.String(3), nullable=False)

    flight_departures = db.relationship("FlightModel", foreign_keys="FlightModel.departure_id", lazy="dynamic")
    flight_destinations = db.relationship("FlightModel", foreign_keys="FlightModel.destination_id", lazy="dynamic")
