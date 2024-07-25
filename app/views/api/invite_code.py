from flask import Blueprint
from werkzeug.exceptions import NotFound
from flask_jwt_extended import current_user, jwt_required
from app.models.invite_code import InviteCode
from app.schemas.invite_code import InviteCodeSchema, invite_code_schema
from app.views import api_view, paginator

api_invite_code_bp = Blueprint('api_invite_code', __name__, url_prefix='/api')

@api_invite_code_bp.route('/invite_codes', methods=['GET'])
@jwt_required()
@api_view()
@paginator(InviteCodeSchema)
def invite_codes_view():
    return InviteCode.query.filter_by(owner_id=current_user.id, deleted=False)

@api_invite_code_bp.route('/invite_codes', methods=['POST'])
@jwt_required()
@api_view()
def create_invite_codes_view():
    invite_code = InviteCode.gene_invite_code(current_user.id)
    if invite_code:
        return invite_code_schema.dump(invite_code)
    else:
        raise Exception("邀请码创建失败")
 
@api_invite_code_bp.route('/invite_codes/<int:invite_code_id>', methods=['GET'])
@jwt_required()
@api_view()
def invite_code_view(invite_code_id):
    invite_code = InviteCode.query.filter_by(owner_id=current_user.id, deleted=False, id=invite_code_id).first()
    if not invite_code:
        raise NotFound("邀请码不存在")
        
    invite_code = invite_code_schema.dump(invite_code)
    return invite_code