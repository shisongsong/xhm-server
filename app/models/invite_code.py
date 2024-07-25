from datetime import datetime
from app import db
from app.libs.eazy_generator import generate_random_string

class InviteCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)
    pieces = db.Column(db.Integer, default=0)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref='invite_codes', foreign_keys=[owner_id])
    
    def gene_invite_code(owner_id, pieces=3):
        invite_code = InviteCode(
            owner_id=owner_id,
            pieces=pieces
        )
        invite_code.code = generate_random_string(6)
        if InviteCode.query.filter(InviteCode.code == invite_code.code).first():
            InviteCode.gene_invite_code(owner_id, pieces)
        else:
            db.session.add(invite_code)
        return invite_code
            
    def consume(self):
        if self.pieces > 0:
            self.pieces -= 1
        else:
            raise Exception("邀请码无效")