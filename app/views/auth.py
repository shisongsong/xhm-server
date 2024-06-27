from flask import Blueprint, request, jsonify, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.exceptions import BadRequest, NotFound
from app.controllers.auth_controller import register, login, get_user_jwt

auth_bp = Blueprint('auth_api', __name__)

class RegistrationForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

@auth_bp.route("/api/register", methods=['POST'])
def register_view():
    json_data = request.get_json()
    if not json_data:
        raise BadRequest("缺少必要参数")
    
    form = RegistrationForm(data=json_data)
    if form.validate_on_submit():
        if register(form.phone.data, form.password.data):
            return jsonify({"message": "Account created successfully!"}), 201
        else:
            return jsonify({"error": "Failed to create account."}), 400
    else:
        errors = {field: error for field, error in form.errors.items()}
        return jsonify({"errors": errors}), 400

@auth_bp.route('/<prefix>/login', methods=['POST'])
def login_view(prefix):
    if prefix not in ["admin", "api"]:
        raise NotFound("api路径不存在")

    json_data = request.get_json()
    if not json_data:
        raise BadRequest("缺少必要参数")
    
    form = LoginForm(data=json_data)
    if form.validate_on_submit():
        user = login(form.phone.data, form.password.data)
        if user:
            access_token = get_user_jwt(user.id)  # 假设get_user_jwt接受用户ID
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        errors = {field: error for field, error in form.errors.items()}
        return jsonify({"errors": errors}), 400