from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from factory import ResponseFactory
from models import AircraftModel
from schemas import AircraftSchema


class Aircraft(Resource):
    _schema = AircraftSchema()
    _response_factory = ResponseFactory("Aircraft")

    @classmethod
    def post(cls, brand: str):
        data = request.get_json()
        if AircraftModel.find_by_brand_and_model(brand, data["model"]):
            return cls._response_factory.error_already_exists("name")

        return cls._insert_new(AircraftModel(brand, data["model"]))

    @classmethod
    def get(cls, brand: str):
        if aircrafts := AircraftModel.find_by_brand(brand):
            if model := request.args.get("model"):
                aircraft = AircraftModel.find_by_brand_and_model(brand, model)
                aircrafts = [aircraft] if aircraft else []
            return {"aircrafts": [cls._json(aircraft) for aircraft in aircrafts]}
        return cls._response_factory.error_not_found()

    @classmethod
    def put(cls, brand: str):
        model = request.args.get("model")
        data = request.get_json()
        if model and (aircraft := AircraftModel.find_by_brand_and_model(brand, model)):
            aircraft.brand = data.get("brand", brand)
            aircraft.model = data.get("model", model)
        else:
            aircraft = AircraftModel(brand, data.get("model", model))

        return cls._insert_new(aircraft)

    @classmethod
    def delete(cls, brand: str):
        model = request.get_json().get("model")
        if model and (aircraft := AircraftModel.find_by_brand_and_model(brand, model)):
            aircraft.delete_from_db()
            return cls._response_factory.ok_deleted()

        if not model and (aircrafts := AircraftModel.find_by_brand(brand)):
            for aircraft in aircrafts:
                aircraft.delete_from_db()
            return cls._response_factory.ok_deleted(plural=True)

        return cls._response_factory.error_not_found()

    @classmethod
    def _insert_new(cls, aircraft: AircraftModel):
        try:
            aircraft.save_to_db()
        except SQLAlchemyError as err:
            return cls._response_factory.error_inserting()

        return cls._response_factory.ok_created(cls._json(aircraft))

    @classmethod
    def _json(cls, obj: AircraftModel):
        return cls._schema.dump(obj)


class AircraftList(Resource):
    _schema = AircraftSchema(many=True)

    @classmethod
    def get(cls):
        return cls._schema.dump(AircraftModel.find_all())
