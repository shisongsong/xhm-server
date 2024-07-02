from flask_jwt_extended import JWTManager

def add_claims_to_access_token(identity):
    from app.models.user import User
    
    user = identity
    if user and user.role:
        return {"role": user.role}
    return {}

def user_identity_lookup(user):
    return user.id

def user_lookup_callback(_jwt_header, jwt_data):
    from app.models.user import User
    
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()