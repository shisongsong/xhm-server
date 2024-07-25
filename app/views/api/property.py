from flask import Blueprint
from werkzeug.exceptions import NotFound
from flask_jwt_extended import current_user, jwt_required
from app.models.property import Property
from app.schemas.property import PropertySchema, property_schema
from app.views import api_view, paginator
from datetime import datetime

api_property_bp = Blueprint('api_property', __name__, url_prefix='/api')

@api_property_bp.route('/properties', methods=['GET'])
@jwt_required()
@api_view()
@paginator(PropertySchema)
def properties_view():
    properties = Property.query.filter_by(deleted=False, user_id=current_user.id).order_by(Property.created_at.desc())
    return properties

@api_property_bp.route('/properties/summary', methods=['GET'])
@jwt_required()
@api_view()
def summary_view():
    properties = Property.query.filter_by(deleted=False, user_id=current_user.id)
    duration_ps = properties.filter_by(ptype=1).filter(Property.end_at >= datetime.now()).order_by(Property.start_at).all()
    pieces_ps = properties.filter_by(ptype=0).filter(Property.pieces >0).all()
    start_at = None
    end_at = None
    pieces = 0
    if duration_ps:
        start_at = duration_ps[0].start_at.isoformat()
        end_at = duration_ps[-1].end_at.isoformat()
    if pieces_ps:
        pieces = sum(p.pieces for p in pieces_ps)
    good_cat = bool (end_at and (datetime.fromisoformat(end_at) > datetime.now() or pieces > 0))
    summary = {'good_cat': good_cat, 'start_at': start_at, 'end_at': end_at, 'pieces': pieces}
    return {'summary': summary}

@api_property_bp.route('/properties/<int:property_id>', methods=['GET'])
@jwt_required()
@api_view()
def property_view(property_id):
    property = Property.query.filter_by(deleted=False, user_id=current_user.id, id=property_id).one_or_none()
    if not property:
        raise NotFound("资产不存在")
        
    property = property_schema.dump(property)
    return property