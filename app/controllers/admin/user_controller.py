from flask import current_app
from app.models.user import User
from app import db

def create(phone, password, role):
    if User.query.filter_by(phone=phone).first():
        current_app.logger.error('Phone already exists.')
        return False
    new_user = User(phone=phone, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return True