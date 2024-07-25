def add_claims_to_access_token(identity):
    user = identity
    if user and user.role:
        return {"role": user.role}
    return {}

def token_verification_callback(_jwt_header, jwt_data):
    from app.models.user import User
    identity = jwt_data["sub"]
    user = User.query.filter_by(deleted=False, id=identity).one_or_none()
    if user:
        return True
    else:
        return False

def user_identity_lookup(user):
    return user.id

def user_lookup_callback(_jwt_header, jwt_data):
    from app.models.user import User
    identity = jwt_data["sub"]
    return User.query.filter_by(deleted=False, id=identity).one_or_none()

def check_if_token_in_blacklist(jwt_header, jwt_data):
    from app.models.revoked_token import RevokedToken
    jti = jwt_data['jti']
    return RevokedToken.is_jti_blacklisted(jti)