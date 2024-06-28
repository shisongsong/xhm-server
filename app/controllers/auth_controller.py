from datetime import timedelta
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.exceptions import BadRequest, NotFound
from app import db
from app.models.user import User

def get_user_jwt(user_id):
    """生成JWT令牌"""
    access_token = create_access_token(identity=user_id, expires_delta=timedelta(hours=2))
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

class RegistrationForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', "密码不一致")])

class LoginForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])