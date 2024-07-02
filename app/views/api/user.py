from flask import Blueprint
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound
from app.models.user import User
from app.schemas.user import user_schema
from app.views import api_view

api_user_bp = Blueprint('api_user', __name__)

@api_user_bp.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
@api_view()
def user_view(user_id):
    user = User.query.get({"id": user_id})
    if not user:
        raise NotFound("用户不存在")
    user = user_schema.dump(user)
    return user