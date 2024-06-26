from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import logging
from logging.handlers import RotatingFileHandler
from app.jwt_callbacks import add_claims_to_access_token
import config
import os

# 初始化app
app = Flask(__name__)
app.config.from_object(config)

# 初始化数据库
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 初始化Marshmallow
ma = Marshmallow(app)

from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.property import Property

# 添加admin用户
with app.app_context():
    u = User.query.filter_by(phone='17696021211').first()
    if u:
        u.set_password('11111111')
        u.role = 'admin'
    else:
        u = User(phone='17696021211', role='admin')
        u.set_password("11111111")
        db.session.add(u)
    db.session.commit()

# 禁用CSRF
app.config['WTF_CSRF_ENABLED'] = False

# JWT配置
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 应替换为强随机密钥
jwt = JWTManager(app)
jwt.additional_claims_loader(add_claims_to_access_token)

# 注册admin Blueprint
from app.views.admin.user import admin_user_bp
app.register_blueprint(admin_user_bp)

# 注册Blueprint
from app.views.auth import auth_bp
from app.views.user import user_bp
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

# 设置日志级别
app.logger.setLevel(logging.DEBUG)  # 或者logging.INFO, logging.WARNING等

# 配置日志文件
if not os.path.exists('logs'):
    os.mkdir('logs')  # 确保logs目录存在
log_file = 'logs/app.log'
file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024*10, backupCount=10)  # 文件大小限制和备份计数
file_handler.setLevel(logging.DEBUG)  # 设置文件日志级别

# 配置控制台日志
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 控制台日志级别，可以根据需要调整

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器到logger
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)