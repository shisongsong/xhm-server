from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from app import db
from app.models.invite_code import InviteCode

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Text, nullable=False, default="user")
    invite_code_code = db.Column(db.String(64))
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # 处理注册邀请码
    def check_invite_code(self, invite_code_code):
        if invite_code_code:
            invite_code = InviteCode.query.filter(InviteCode.code == invite_code_code, InviteCode.pieces > 0).first()
            if invite_code:
                invite_code.consume()
                self.invite_code_code = invite_code.code
            else:
                raise NotFound("邀请码不存在")