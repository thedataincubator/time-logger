from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def gen_dt(cls, window):
        return datetime.utcnow() + timedelta(days=-window)
