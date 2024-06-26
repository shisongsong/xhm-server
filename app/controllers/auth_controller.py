from flask import current_app
from app.models.user import User
from flask_jwt_extended import create_access_token
from app import db

def get_user_jwt(user_id):
    """生成JWT令牌"""
    access_token = create_access_token(identity=user_id)
    return access_token

def register(phone, password):
    if User.query.filter_by(phone=phone).first():
        current_app.logger.error('Phone already exists.')
        return False
    new_user = User(phone=phone)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return True

def login(phone, password):
    user = User.query.filter_by(phone=phone, deleted=False).first()
    if user and user.check_password(password):
        return user
    return None