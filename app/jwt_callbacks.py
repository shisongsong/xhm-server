from models.user import User

def add_claims_to_access_token(identity):
    user = User.query.get(identity)
    if user and user.role:
        return {"role": user.role}
    return {}