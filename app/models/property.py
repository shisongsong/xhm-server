from app import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    ptype = db.Column(db.Integer, default=0)
    price = db.Column(db.Decimal, defaul=0)
    pieces = db.Column(db.Integer, default=0)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
