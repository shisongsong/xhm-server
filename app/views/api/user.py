from flask import Blueprint
from flask_jwt_extended import current_user, jwt_required
from werkzeug.exceptions import NotFound
from app.models.user import User
from app.schemas.user import user_schema
from app.views import api_view

api_user_bp = Blueprint('api_user', __name__)

@api_user_bp.route('/api/users/me', methods=['GET'])
@jwt_required()
@api_view()
def user_view():
    user:User = current_user
    if not user:
        raise NotFound("用户不存在")
    user = user_schema.dump(user)
    return {'user': user}