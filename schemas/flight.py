import constants.schema
from models import FlightModel
from serialization import serializer


class FlightSchema(serializer.SQLAlchemyAutoSchema):
    class Meta:
        model = FlightModel
        load_only = constants.schema.LOAD_ONLY + ("departure", "destination", "airline", "aircraft")
        dump_only = constants.schema.DUMP_ONLY
        include_fk = True
