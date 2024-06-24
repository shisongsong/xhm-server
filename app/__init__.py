from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import logging
from logging.handlers import RotatingFileHandler
import config
import os

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.views.auth import auth_bp
from app.views.user import user_bp
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

# JWT配置
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 应替换为强随机密钥
jwt = JWTManager(app)

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