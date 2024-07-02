from flask import Blueprint
from werkzeug.exceptions import NotFound
from flask_jwt_extended import current_user, jwt_required
from app.models.property import Property
from app.schemas.property import PropertySchema, properties_schema, property_schema
from app.views import api_view, paginator

api_property_bp = Blueprint('api_property', __name__, url_prefix='/api')

@api_property_bp.route('/properties', methods=['GET'])
@jwt_required()
@api_view()
@paginator(PropertySchema)
def properties_view():
    properties = Property.query.filter_by(deleted=False, uesr_id=current_user.id).order_by(Property.created_at.desc())
    return properties_schema.dump(properties)

@api_property_bp.route('/properties/<int:property_id>', methods=['GET'])
@jwt_required()
@api_view()
def property_view(property_id):
    property = Property.query.filter_by(deleted=False, uesr_id=current_user.id).get({"id": property_id})
    if not property:
        raise NotFound("资产不存在")
        
    property = property_schema.dump(property)
    return property