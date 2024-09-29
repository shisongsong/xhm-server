from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.exceptions import Unauthorized, Conflict
from app import db
from app.models.invite_code import InviteCode
from app.models.user import User
from app.schemas.user import user_schema

def get_user_jwt(user, refresh=False):
    """生成JWT令牌"""
    access_token = create_access_token(identity=user, expires_delta=timedelta(hours=2))
    refresh_token = None
    if refresh:
        refresh_token = create_refresh_token(identity=user, expires_delta=timedelta(days=30))
    return access_token, refresh_token

def register(json_data):
    form:RegistrationForm = RegistrationForm(data=json_data)
    if form.validate_on_submit():
        with db.session.begin():
            if User.query.filter_by(phone=form.phone.data).first():
                raise Conflict("手机号已存在，请更换手机号重试")
            new_user = User(phone=form.phone.data)
            new_user.set_password(form.password.data)
            new_user.check_invite_code(form.invite_code_code.data)
            db.session.add(new_user)
            db.session.flush()
            # 生成自己的邀请码
            InviteCode.gene_invite_code(new_user.id)
        return login(json_data)
    else:
        errors = {field: error for field, error in form.errors.items()}
        return errors, None

def login(json_data):
    form:LoginForm = LoginForm(data=json_data)
    if form.validate_on_submit():
        user:User = User.query.filter_by(phone=form.phone.data, deleted=False).first()
        if user and user.check_password(form.password.data):
            access_token, refresh_token = get_user_jwt(user, True)
            return None, { 'access_token': access_token, 'refresh_token': refresh_token, 'user': user_schema.dump(user) }
        else:
            raise Unauthorized("用户名或密码错误")
    else:
        errors = {field: error for field, error in form.errors.items()}
        return errors, None
    
class RegistrationForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', "密码不一致")])
    invite_code_code = StringField('Invite Code')

class LoginForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])