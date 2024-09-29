from datetime import datetime
from app import db

class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
    refresh_token = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def add(self):
        db.session.add(self)

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
    
    @classmethod
    def is_token_blacklisted(cls, refresh_token):
        query = cls.query.filter_by(refresh_token=refresh_token).first()
        return bool(query)