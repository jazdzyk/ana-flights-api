from importlib.resources import Resource

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from factory import ResponseFactory
from models import AirportModel
from schemas import AirportSchema


class Airport(Resource):
    _schema = AirportSchema()
    _response_factory = ResponseFactory("Airport")

    @classmethod
    def post(cls, iata: str):
        if AirportModel.find_by_iata(iata):
            return cls._response_factory.error_already_exists("iata")

        data = request.get_json()
        new_airport = AirportModel(data["name"], iata, data["country"])
        return cls._insert_new(new_airport)

    @classmethod
    def get(cls, iata: str):
        if airport := AirportModel.find_by_iata(iata):
            return cls._json(airport)
        return cls._response_factory.error_not_found()

    @classmethod
    def put(cls, iata: str):
        data = request.get_json()
        if airport := AirportModel.find_by_iata(iata):
            airport.iata = data.get("iata", iata)
            airport.name = data.get("name", airport.name)
            airport.country = data.get("country", airport.country)
        else:
            airport = AirportModel(iata, data["name"], data["country"])

        return cls._insert_new(airport)

    @classmethod
    def delete(cls, iata: str):
        if airport := AirportModel.find_by_iata(iata):
            airport.delete_from_db()
            return cls._response_factory.ok_deleted()
        return cls._response_factory.error_not_found()

    @classmethod
    def _insert_new(cls, airport: AirportModel):
        try:
            airport.save_to_db()
        except SQLAlchemyError as err:
            return cls._response_factory.error_inserting()

    @classmethod
    def _json(cls, obj: AirportModel):
        return cls._schema.dump(obj)


class AirportByCountry(Resource):
    _schema = AirportSchema(many=True)

    @classmethod
    def get(cls, country: str):
        return cls._schema.dump(AirportModel.find_by_country(country))


class AirportList(Resource):
    _schmea = AirportSchema()

    @classmethod
    def get(cls):
        return cls._schmea.dump(AirportModel.find_all())
