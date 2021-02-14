from models import AirlineModel
from schemas import FlightSchema
from serialization import serializer
import constants.schema


class AirlineSchema(serializer.SQLAlchemyAutoSchema):
    flights = serializer.Nested(FlightSchema, many=True)

    class Meta:
        model = AirlineModel
        load_only = constants.schema.LOAD_ONLY
        dump_only = constants.schema.DUMP_ONLY
        fk_include = True
