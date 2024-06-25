from flask import Blueprint, jsonify, request, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_jwt_extended import jwt_required
from jwt_required import admin_route_required
from app.models.user import User
from app.schemas.user import users_schema, user_schema

admin_user_bp = Blueprint('user', __name__, url_prefix='/admin')

class CreateUserForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])

@admin_user_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_route_required
def users_view():
    all_users = User.query.all()
    users = users_schema.dumps(all_users)
    return users, 201

@admin_user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_route_required
def user_view(user_id):
    user = user_schema.dumps(User.query.get({"id": user_id}))
    return user, 201


@admin_user_bp.route('/users', methods=['POST'])
@jwt_required()
@admin_route_required
def create_user():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    current_app.logger.info(json_data)
    form = CreateUserForm(data=json_data)
    if form.validate_on_submit():
        if register(form.phone.data, form.password.data):
            return jsonify({"message": "Account created successfully!"}), 201
        else:
            return jsonify({"error": "Failed to create account."}), 400
    else:
        errors = {field: error for field, error in form.errors.items()}
        return jsonify({"errors": errors}), 400
    