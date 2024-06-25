from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    ptype = db.Column(db.Integer, default=0)
    price = db.Column(db.Decimal, defaul=0)
    pieces = db.Column(db.Integer, default=0)
    duration = db.Column(db.Integer, default=0)
