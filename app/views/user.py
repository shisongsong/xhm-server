from flask import Blueprint, request, jsonify, current_app
from app.controllers.user_controller import get_all
from app.models.user import User

user_bp = Blueprint('user_api', __name__)

@user_bp.route('/api/users', methods=['GET'])
def users_view():
    users = get_all()
    return jsonify(users), 201

@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def user_view(user_id):
    user = User.query.filter_by(id = user_id)
    return jsonify(user), 201