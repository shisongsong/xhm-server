
from flask_sqlalchemy import SQLAlchemy
from app.models.user import User
from app.models.product import Product

def seed_data(app, db:SQLAlchemy):
    with app.app_context():  # 确保在应用上下文中操作数据库
        u:User = User.query.filter_by(phone='17696021211').first()
        if u:
            u.set_password('11111111')
            u.role = 'admin'
        else:
            u = User(phone='17696021211', role='admin')
            u.set_password("11111111")
            db.session.add(u)
        product1:Product = Product.query.filter_by(ptype=0, pieces=1, deleted=False).first()
        if not product1:
            p1 = Product(
                name='1次',
                description='1次',
                ptype=0,
                price=68,
                pieces=1
            )
            db.session.add(p1)
            
        product2:Product = Product.query.filter_by(ptype=1, duration=30, deleted=False).first()
        if not product2:
            p2 = Product(
                name='30天',
                description='30天',
                ptype=1,
                price=268,
                duration=30
            )
            db.session.add(p2)
        db.session.commit()