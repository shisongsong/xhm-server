from app import ma
from app.models.property import Property
from marshmallow.fields import Nested

from app.schemas.product import ProductSchema
from app.schemas.user import UserSchema
class PropertySchema(ma.SQLAlchemyAutoSchema):
    user = Nested(UserSchema.Meta, only=['id', 'phone', 'role'])
    product = Nested(ProductSchema, only=['id', 'name', 'description', 'ptype', 'pieces', 'duration', 'price'])
    class Meta:
        model = Property
        include_fk = True

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)