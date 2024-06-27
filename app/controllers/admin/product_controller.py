from flask import current_app
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, IntegerField, StringField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.exceptions import BadRequest, NotFound
from app.models.product import Product
from app import db

def create(json_data):
    form:CreateProductForm = CreateProductForm(data=json_data)
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            ptype=form.ptype.data,
            pieces=form.pieces.data,
            price=form.price.data,
            duration=form.duration.data
        )
        db.session.add(new_product)
        db.session.commit()
    else:
        errors = {field: error for field, error in form.errors.items()}
        return errors

def update(product_id, json_data):
    product = Product.query.get(product_id)
    if not product:
        raise NotFound("产品不存在")
    form:UpdateProductForm = UpdateProductForm(data=json_data)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.ptype = form.ptype.data
        product.pieces = form.pieces.data
        product.price = form.price.data
        product.duration = form.duration.data
        product.deleted = form.deleted.data
        db.session.commit()
    else:
        errors = {field: error for field, error in form.errors.items()}
        return errors

class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    ptype = IntegerField('Ptype', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    pieces = IntegerField('Pieces', default=0)
    duration = IntegerField('Duration', default=0)
    
class UpdateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    ptype = IntegerField('Ptype', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    pieces = IntegerField('Pieces', default=0)
    duration = IntegerField('Duration', default=0)
    deleted = BooleanField('Deleted', default=False)