from app import ma
from app.models.invite_code import InviteCode
from marshmallow.fields import Nested
from app.schemas.user import UserSchema

class InviteCodeSchema(ma.SQLAlchemyAutoSchema):
    owner = Nested(UserSchema, only=['id', 'phone', 'role'])
    users = Nested(UserSchema, only=['id', 'phone', 'role'], many=True)
    class Meta:
        model = InviteCode

invite_code_schema = InviteCodeSchema()
invite_codes_schema = InviteCodeSchema(many=True)