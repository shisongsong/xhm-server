from flask import jsonify, make_response, current_app
from functools import wraps
from werkzeug.exceptions import HTTPException

def api_view():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 调用原始的视图函数
                result = func(*args, **kwargs)
                
                # 如果视图函数返回的是元组，假设第一个元素是数据，第二个是状态码
                if isinstance(result, tuple):
                    success, data, status_code = result
                    return make_response({'success': success, 'data': data}, status_code)
                
                # 否则，使用默认的状态码200
                return make_response({'success': True, 'data': result}, 200)
            
            except Exception as e:
                current_app.logger.error(e)
                
                # 根据异常类型返回不同的状态码
                if isinstance(e, KeyError):
                    return make_response(jsonify({'success': False, 'message': str(e)}), 400)
                elif isinstance(e, HTTPException):
                    return make_response(jsonify({'success': False, 'message': str(e)}), e.code)
                
                # 其他未处理的异常，返回500 Internal Server Error
                return make_response(jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500)
        
        return wrapper
    return decorator