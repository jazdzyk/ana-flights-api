from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

import factory.responses
from models import AircraftModel
from schemas import AircraftSchema


class Aircraft(Resource):
    _schema = AircraftSchema()

    @classmethod
    def post(cls, brand: str):
        data = request.get_json()
        if AircraftModel.find_by_brand_and_model(brand, data["model"]):
            return factory.responses.error_already_exists(cls.__name__, "name")

        return cls._insert_new(AircraftModel(brand, data["model"]))

    @classmethod
    def get(cls, brand: str):
        if aircrafts := AircraftModel.find_by_brand(brand):
            if model := request.args.get("model"):
                aircraft = AircraftModel.find_by_brand_and_model(brand, model)
                aircrafts = [aircraft] if aircraft else []
            return {"aircrafts": [cls._json(aircraft) for aircraft in aircrafts]}
        return factory.responses.error_not_found(cls.__name__)

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
            return factory.responses.ok_deleted(cls.__name__)

        if not model and (aircrafts := AircraftModel.find_by_brand(brand)):
            for aircraft in aircrafts:
                aircraft.delete_from_db()
            return factory.responses.ok_deleted(cls.__name__, plural=True)

        return factory.responses.error_not_found(cls.__name__)

    @classmethod
    def _insert_new(cls, new_obj: AircraftModel):
        try:
            new_obj.save_to_db()
        except SQLAlchemyError as err:
            return factory.responses.error_inserting(cls.__name__)

        return factory.responses.ok_created(cls._json(new_obj))

    @classmethod
    def _json(cls, obj: AircraftModel):
        return cls._schema.dump(obj)


class AircraftList(Resource):
    _schema = AircraftSchema(many=True)

    @classmethod
    def get(cls):
        return cls._schema.dump(AircraftModel.find_all())
