from db import db
from models import BaseModel


class FlightModel(BaseModel):
    __tablename__ = "flights"

    date = db.Column(db.Date, nullable=False)
    distance = db.Column(db.Integer)

    departure_id = db.Column(db.Integer, db.ForeignKey("airports.id"), nullable=False)
    departure = db.relationship("AirportModel", foreign_keys=departure_id)

    destination_id = db.Column(db.Integer, db.ForeignKey("airports.id"), nullable=False)
    destination = db.relationship("AirportModel", foreign_keys=destination_id)

    airline_id = db.Column(db.Integer, db.ForeignKey("airlines.id"), nullable=False)
    airline = db.relationship("AirlineModel")

    aircraft_id = db.Column(db.Integer, db.ForeignKey("aircrafts.id"), nullable=False)
    aircraft = db.relationship("AircraftModel")
