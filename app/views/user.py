from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models.user import User
from app.schemas.user import users_schema, user_schema

user_bp = Blueprint('user_api', __name__)

@user_bp.route('/api/users', methods=['GET'])
def users_view():
    all_users = User.query.all()
    users = users_schema.dumps(all_users)
    return users, 201

@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def user_view(user_id):
    user = user_schema.dumps(User.query.get({"id": user_id}))
    return user, 201