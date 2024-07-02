from flask import Blueprint, current_app, request
from werkzeug.exceptions import BadRequest, NotFound
from flask_jwt_extended import get_jwt, jwt_required
from app.controllers.admin.user_controller import create, send_gift, update, reset_password
from app.jwt_required import admin_route_required
from app.models.user import User
from app.schemas.user import UserSchema, user_schema
from app.views import api_view, paginator

admin_user_bp = Blueprint('admin_user', __name__, url_prefix='/admin')

@admin_user_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_route_required
@api_view()
@paginator(UserSchema)
def users_view():
    query = User.query
    phone = request.args.get('phone', '')
    role = request.args.get('role', '')
    if phone:
        query = query.filter(User.phone.like(f'%{phone}%'))
    if request.args.get('role'):
        query = query.filter_by(role = role)
    return query

@admin_user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_route_required
@api_view()
def user_view(user_id):
    user = User.query.get({"id": user_id})
    if not user:
        raise NotFound("用户不存在")
        
    user = user_schema.dump(user)
    return user

@admin_user_bp.route('/users', methods=['POST'])
@jwt_required()
@admin_route_required
@api_view()
def create_view():
    json_data = request.get_json()
    if not json_data:
        raise BadRequest("缺少必要参数")

    errors = create(json_data)
    return not errors, {"errors": errors}, 200
    
@admin_user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_route_required
@api_view()
def update_view(user_id):
    json_data = request.get_json()
    if not json_data or not user_id:
        raise BadRequest("缺少必要参数")

    errors = update(user_id, json_data)
    return not errors, {"errors": errors}, 200

@admin_user_bp.route('/users/<int:user_id>/reset_password', methods=['PUT'])
@jwt_required()
@admin_route_required
@api_view()
def reset_password_view(user_id):
    json_data = request.get_json()
    if not json_data or not user_id:
        raise BadRequest("缺少必要参数")

    errors = reset_password(user_id, json_data)
    return not errors, {"errors": errors}, 200

@admin_user_bp.route('/users/<int:user_id>/send_gift', methods=['POST'])
@jwt_required()
@admin_route_required
@api_view()
def send_gift_view(user_id):
    json_data = request.get_json()
    if not json_data or not user_id:
        raise BadRequest("缺少必要参数")

    errors = send_gift(user_id, json_data)
    return not errors, {"errors": errors}, 200