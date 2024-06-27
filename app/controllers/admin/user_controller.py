from flask import current_app
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.exceptions import BadRequest, NotFound
from app.models.user import User
from app import db

def create(json_data):
    form:CreateUserForm = CreateUserForm(data=json_data)
    if form.validate_on_submit():
        if User.query.filter_by(phone=form.phone.data).first():
            raise BadRequest("手机号已存在")
    
        new_user = User(phone=form.phone.data, role=form.role.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
    else:
        errors = {field: error for field, error in form.errors.items()}
        return errors

def update(user_id, json_data):
    user = User.query.get(user_id)
    if not user:
        raise NotFound("用户不存在")
    form:UpdateUserForm = UpdateUserForm(data=json_data)
    if form.validate_on_submit():
        user.phone = form.phone.data
        user.role = form.role.data
        user.deleted = form.deleted.data
        db.session.commit()
    else:
        errors = {field: error for field, error in form.errors.items()}
        return errors
    
def reset_password(user_id, json_data):
    user = User.query.get(user_id)
    if not user:
        raise NotFound("用户不存在")
    form:ResetPasswordForm = ResetPasswordForm(data=json_data)
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
    else:
        errors = {field: error for field, error in form.errors.items()}
        return errors

class CreateUserForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    
class UpdateUserForm(FlaskForm):
    phone = StringField('Phone')
    role = StringField('Role')
    deleted = BooleanField('Deleted')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password', message="密码不一致")])