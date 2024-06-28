from flask import Blueprint, request, current_app
from werkzeug.exceptions import BadRequest, NotFound
from flask_jwt_extended import jwt_required
from app.controllers.admin.property_controller import update
from app.jwt_required import admin_route_required
from app.models.property import Property
from app.schemas.property import properties_schema, property_schema
from app.views import api_view

admin_property_bp = Blueprint('property', __name__, url_prefix='/admin')

@admin_property_bp.route('/properties', methods=['GET'])
@jwt_required()
@admin_route_required
@api_view()
def properties_view():
    all_properties = Property.query.all()
    properties = properties_schema.dump(all_properties)
    return properties

@admin_property_bp.route('/properties/<int:property_id>', methods=['GET'])
@jwt_required()
@admin_route_required
@api_view()
def property_view(property_id):
    property = Property.query.get({"id": property_id})
    if not property:
        raise NotFound("产品不存在")
        
    property = property_schema.dump(property)
    return property

@admin_property_bp.route('/properties/<int:property_id>', methods=['PUT'])
@jwt_required()
@admin_route_required
@api_view()
def update_view(property_id):
    json_data = request.get_json()
    if not json_data or not property_id:
        raise BadRequest("缺少必要参数")

    errors = update(property_id, json_data)
    return not errors, {"errors": errors}, 200