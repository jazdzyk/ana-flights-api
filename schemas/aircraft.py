import constants.schema
from models import AircraftModel
from serialization import serializer


class AircraftSchema(serializer.SQLAlchemyAutoSchema):
    class Meta:
        model = AircraftModel
        load_only = constants.schema.LOAD_ONLY
        dump_only = constants.schema.DUMP_ONLY
        include_fk = True
