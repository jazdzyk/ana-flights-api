from typing import List

from db import db
from models import BaseModel


class AirlineModel(db.Model, BaseModel):
    __tablename__ = "airlines"

    name = db.Column(db.String(50), nullable=False, unique=True)

    flights = db.relationship("FlightModel", foreign_keys="FlightModel.airline_id", lazy="dynamic")

    def __init__(self, name: str):
        BaseModel.__init__(self)
        self.name = name

    @classmethod
    def find_by_name(cls, name: str) -> "AirlineModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["AirlineModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
