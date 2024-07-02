from datetime import datetime
from app import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    ptype = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0)
    pieces = db.Column(db.Integer, default=0)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, default=-1)
    
    user = db.relationship('User', backref='properties')
    product = db.relationship('Product', backref='properties')
    order = db.relationship('Order', backref='properties')
