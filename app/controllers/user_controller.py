from app.models.user import User
from app.schemas.user import users_schema

def get_all():
    all_users = User.query.all()
    return users_schema.dump(all_users)