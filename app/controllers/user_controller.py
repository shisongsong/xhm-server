from app.models.user import User

def get_all():
    users =  User.query.all()
    return users