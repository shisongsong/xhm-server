from datetime import datetime
from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    ptype = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0)
    pieces = db.Column(db.Integer, default=0)
    duration = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)