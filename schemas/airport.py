import constants.schema
from models import AirportModel
from serialization import serializer


class AirportSchema(serializer.SQLAlchemyAutoSchema):
    class Meta:
        model = AirportModel
        load_only = constants.schema.LOAD_ONLY
        dump_only = constants.schema.DUMP_ONLY
        include_fk = True
