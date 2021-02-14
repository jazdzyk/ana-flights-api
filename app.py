from flask import Flask
from flask_restful import Api

from constants import config, endpoints
from db import db
from serialization import serializer


def configure_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app


def configure_api(app):
    api = Api(app)

    endpoints_list = [getattr(endpoints, name) for name in dir(endpoints) if name.isupper()]
    for endpoint_info in endpoints_list:
        api.add_resource(*endpoint_info)


if __name__ == '__main__':
    app = configure_app()
    configure_api(app)

    db.init_app(app)
    serializer.init_app(app)

    app.run(port=config.APP_PORT, debug=config.DEBUG)
