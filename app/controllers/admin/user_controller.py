from datetime import datetime, timedelta
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.exceptions import BadRequest, NotFound
from app.models.product import Product
from app.models.property import Property
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
    
def send_gift(user_id:int, json_data):
    user = User.query.get(user_id)
    if not user:
        raise NotFound("用户不存在")
    form:SendGiftForm = SendGiftForm(data=json_data)
    if form.validate_on_submit():
        product:Product = Product.query.get(form.product_id.data)
        if not product:
            raise NotFound("产品不存在")
        last_property:Property = Property.query.filter_by(user_id = user_id, ptype=1, deleted=False).first()
        start_at, end_at = None, None
        
        if product.ptype == 1:
            start_at = datetime.now()
            if last_property and last_property.end_at > datetime.now():
                start_at = last_property.end_at
            end_at = start_at + timedelta(days = product.duration)
            
        new_property:Property = Property(
            name=product.name,
            description=product.description,
            ptype=product.ptype,
            price=product.price,
            pieces=product.pieces,
            user_id=user_id,
            product_id=form.product_id.data,
            order_id=-1,
            start_at=start_at,
            end_at=end_at
        )
        db.session.add(new_property)
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
    
class SendGiftForm(FlaskForm):
    product_id = IntegerField('Product', validators=[DataRequired()])