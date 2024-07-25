from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from app.jwt_callbacks import add_claims_to_access_token, check_if_token_in_blacklist, token_verification_callback, user_identity_lookup, user_lookup_callback
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
from app.models.invite_code import InviteCode

# 创建种子数据
from app.seed_data import seed_data
seed_data(app, db)

# 禁用CSRF
app.config['WTF_CSRF_ENABLED'] = False
CORS(app)

# JWT配置
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 应替换为强随机密钥
app.config['JWT_BLACKLIST_ENABLED'] = True     # 启用黑名单功能
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # 在哪些类型的令牌上检查黑名单

jwt = JWTManager(app)
jwt.additional_claims_loader(add_claims_to_access_token)
jwt.token_verification_loader(token_verification_callback)
jwt.user_identity_loader(user_identity_lookup)
jwt.user_lookup_loader(user_lookup_callback)
jwt.token_in_blocklist_loader(check_if_token_in_blacklist)

# 注册Blueprint
from app.views.auth import auth_bp
app.register_blueprint(auth_bp)

# 注册admin Blueprint
from app.views.admin.user import admin_user_bp
from app.views.admin.product import admin_product_bp
from app.views.admin.property import admin_property_bp
from app.views.admin.invite_code import admin_invite_code_bp
app.register_blueprint(admin_user_bp)
app.register_blueprint(admin_product_bp)
app.register_blueprint(admin_property_bp)
app.register_blueprint(admin_invite_code_bp)

# 注册api Blueprint
from app.views.api.user import api_user_bp
from app.views.api.product import api_product_bp
from app.views.api.property import api_property_bp
from app.views.api.invite_code import api_invite_code_bp
app.register_blueprint(api_user_bp)
app.register_blueprint(api_product_bp)
app.register_blueprint(api_property_bp)
app.register_blueprint(api_invite_code_bp)

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
console_handler.setLevel(logging.DEBUG)  # 控制台日志级别，可以根据需要调整

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器到logger
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)