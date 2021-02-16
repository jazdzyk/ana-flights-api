from datetime import datetime
from typing import List

from db import db


class BaseModel:
    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    modified_count = db.Column(db.Integer, nullable=False)

    def __init__(self):
        now = datetime.now()
        self.created = now
        self.last_modified = now
        self.modified_count = 0

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()
