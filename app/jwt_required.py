from functools import wraps
from flask import current_app, jsonify
from flask_jwt_extended import get_jwt

def admin_route_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 获取 JWT 中的 claims
        claims = get_jwt()
        
        # 检查用户角色是否为 'admin'
        if claims.get("role") != "admin":
            return jsonify({"msg": "Admin access required"}), 403
        
        return fn(*args, **kwargs)
    
    return wrapper