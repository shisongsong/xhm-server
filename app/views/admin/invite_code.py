from flask import Blueprint
from werkzeug.exceptions import BadRequest, NotFound
from flask_jwt_extended import jwt_required
from app import db
from app.jwt_required import admin_route_required
from app.models.invite_code import InviteCode
from app.schemas.invite_code import InviteCodeSchema, invite_code_schema
from app.views import api_view, paginator

admin_invite_code_bp = Blueprint('admin_invite_code', __name__, url_prefix='/admin')

@admin_invite_code_bp.route('/invite_codes', methods=['GET'])
@jwt_required()
@admin_route_required
@api_view()
@paginator(InviteCodeSchema)
def invite_codes_view():
    return InviteCode.query

@admin_invite_code_bp.route('/invite_codes/<int:invite_code_id>', methods=['GET'])
@jwt_required()
@admin_route_required
@api_view()
def invite_code_view(invite_code_id):
    invite_code = InviteCode.query.get({"id": invite_code_id})
    if not invite_code:
        raise NotFound("产品不存在")
        
    invite_code = invite_code_schema.dump(invite_code)
    return invite_code

@admin_invite_code_bp.route('/invite_codes/<int:invite_code_id>', methods=['DELETE'])
@jwt_required()
@admin_route_required
@api_view()
def delete_view(invite_code_id):
    if not invite_code_id:
        raise BadRequest("缺少必要参数")
    invite_code = InviteCode.query.get(invite_code_id)
    if invite_code:
        db.session.delete(invite_code)
        db.session.commit()
        return True, {"errors": None }, 200
    else:
        raise NotFound("邀请码不存在")