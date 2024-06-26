def add_claims_to_access_token(identity):
    from app.models.user import User
    
    user = User.query.get(identity)
    if user and user.role:
        return {"role": user.role}
    return {}