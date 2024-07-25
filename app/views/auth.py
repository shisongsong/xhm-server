from flask import Blueprint, request
from flask_jwt_extended import get_jwt, jwt_required
from werkzeug.exceptions import BadRequest, NotFound
from app import db
from app.controllers.auth_controller import get_user_jwt, register, login
from app.models.revoked_token import RevokedToken
from app.models.user import User
from app.schemas.user import user_schema
from app.views import api_view

auth_bp = Blueprint('auth_api', __name__)

@auth_bp.route("/api/register", methods=['POST'])
@api_view()
def register_view():
    json_data = request.get_json()
    if not json_data:
        raise BadRequest("缺少必要参数")
    
    errors, res = register(json_data)
    if not errors:
        return res
    else:
        return not errors, { errors: errors }, 200

@auth_bp.route('/<prefix>/login', methods=['POST'])
@api_view()
def login_view(prefix):
    if prefix not in ["admin", "api"]:
        raise NotFound("api路径不存在")
    json_data = request.get_json()
    if not json_data:
        raise BadRequest("缺少必要参数")
    
    errors, res = login(json_data)
    if not errors:
        return res
    else:
        return not errors, { errors: errors }, 200
    
@auth_bp.route('/<prefix>/refresh', methods=['POST'])
@jwt_required(refresh=True)
@api_view()
def refresh_view(prefix):
    if prefix not in ["admin", "api"]:
        raise NotFound("api路径不存在")
    identity = get_jwt()["sub"]
    user:User = User.query.filter_by(id=identity).one_or_none()
    access_token, refresh_token = get_user_jwt(user)
    return { 'access_token': access_token, 'refresh_token': refresh_token, 'user': user_schema.dump(user) }

@auth_bp.route('/<prefix>/logout', methods=['POST'])
@jwt_required()
@api_view()
def logout_view(prefix):
    if prefix not in ["admin", "api"]:
        raise NotFound("api路径不存在")
    jti = get_jwt()['jti']
    revoked_token = RevokedToken(jti=jti)
    revoked_token.add()
    db.session.commit()
    return {"message": "退出登录"}