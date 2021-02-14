from db import db


class BaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    modified_count = db.Column(db.Integer, nullable=False)
