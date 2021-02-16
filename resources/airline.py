from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

import factory.responses
from models import AirlineModel
from schemas.airline import AirlineSchema


class Airline(Resource):
    _schema = AirlineSchema()

    @classmethod
    def post(cls, name: str):
        if AirlineModel.find_by_name(name):
            return factory.responses.error_already_exists(cls.__name__, "name")
        return cls._insert_new(name)

    @classmethod
    def get(cls, name: str):
        if airline := AirlineModel.find_by_name(name):
            return cls._json(airline)
        return factory.responses.error_not_found(cls.__name__)

    @classmethod
    def put(cls, name: str):
        if airline := AirlineModel.find_by_name(name):
            data = request.get_json()
            airline.name = data["name"]
            try:
                airline.save_to_db()
            except SQLAlchemyError as err:
                return factory.responses.error_inserting(cls.__name__)
            return cls._json(airline)
        else:
            return cls._insert_new(name)

    @classmethod
    def delete(cls, name: str):
        if airline := AirlineModel.find_by_name(name):
            airline.delete_from_db()
            return factory.responses.ok_deleted(cls.__name__)
        return factory.responses.error_not_found(cls.__name__)

    @classmethod
    def _insert_new(cls, name: str):
        new_airline = AirlineModel(name)
        try:
            new_airline.save_to_db()
        except SQLAlchemyError as err:
            return factory.responses.error_inserting(cls.__name__)

        return factory.responses.ok_created(cls._json(new_airline))

    @classmethod
    def _json(cls, obj: AirlineModel):
        return cls._schema.dump(obj)


class AirlineList(Resource):
    _schema = AirlineSchema(many=True)

    @classmethod
    def get(cls):
        return cls._schema.dump(AirlineModel.find_all())
