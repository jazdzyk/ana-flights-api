from typing import List

from db import db
from models import BaseModel


class AirportModel(db.Model, BaseModel):
    __tablename__ = "airports"

    iata = db.Column(db.String(3), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    country = db.Column(db.String(30), nullable=False)

    flight_departures = db.relationship("FlightModel", foreign_keys="FlightModel.departure_id", lazy="dynamic")
    flight_destinations = db.relationship("FlightModel", foreign_keys="FlightModel.destination_id", lazy="dynamic")

    def __init__(self, iata: str, name: str, country: str):
        BaseModel.__init__(self)
        self.iata = iata
        self.name = name
        self.country = country

    @classmethod
    def find_by_iata(cls, iata: str) -> "AirportModel":
        return cls.query.filter_by(iata=iata).first()

    @classmethod
    def find_by_country(cls, country: str) -> List["AirportModel"]:
        return cls.query.filter_by(country=country).all()
