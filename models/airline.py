from db import db
from models import BaseModel


class AirlineModel(BaseModel):
    __tablename__ = "airlines"

    name = db.Column(db.String(50), nullable=False)

    flights = db.relationship("FlightModel", foreign_keys="FlightModel.airline_id", lazy="dynamic")
