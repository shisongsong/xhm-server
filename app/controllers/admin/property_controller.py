from datetime import datetime
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateTimeField, DecimalField, IntegerField, StringField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.exceptions import BadRequest, NotFound
from app.models.property import Property
from app import db

def update(property_id, json_data):
    property:Property = Property.query.get(property_id)
    if not property:
        raise NotFound("资产不存在")
    form:UpdatePropertyForm = UpdatePropertyForm(data=json_data)
    if form.validate_on_submit():
        property.name = form.name.data
        property.description = form.description.data
        property.ptype = form.ptype.data
        property.pieces = form.pieces.data
        property.price = form.price.data
        property.start_at = form.start_at.data
        property.end_at = form.end_at.data
        property.deleted = form.deleted.data
        db.session.commit()
    else:
        errors = {field: error for field, error in form.errors.items()}
        return errors

class UpdatePropertyForm(FlaskForm):
    name = StringField('Name')
    description = StringField('Description')
    price = DecimalField('Price')
    pieces = IntegerField('Pieces')
    start_at = DateTimeField('Start at')
    end_at = DateTimeField('End at')
    deleted = BooleanField("Deleted")