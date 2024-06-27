from flask import Blueprint, jsonify, request, current_app
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.exceptions import BadRequest, NotFound
from flask_jwt_extended import jwt_required
from app.controllers.admin.user_controller import create, update, reset_password, delete
from app.jwt_required import admin_route_required
from app.models.user import User
from app.schemas.user import users_schema, user_schema
from app.views import api_view

admin_user_bp = Blueprint('user', __name__, url_prefix='/admin')

class CreateUserForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    
class UpdateUserForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    deleted = BooleanField('Deleted', validators=[DataRequired()])
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired()])

@admin_user_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_route_required
@api_view()
def users_view():
    all_users = User.query.all()
    users = users_schema.dump(all_users)
    return users

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