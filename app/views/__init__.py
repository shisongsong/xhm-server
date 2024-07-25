from flask import jsonify, make_response, current_app, request
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
                    return make_response(jsonify({'success': False, 'message': str(e.description)}), e.code)
                # 其他未处理的异常，返回500 Internal Server Error
                return make_response(jsonify({'success': False, 'message': '发生了错误'}), 500)
        
        return wrapper
    return decorator

# 分页装饰器
def paginator(schema_class):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 10, type=int), 100)
            
            # 调用原始函数获取查询对象，然后进行分页
            query = func(*args, **kwargs)
            paginated_query = query.paginate(page=page, per_page=per_page, error_out=False)
            
            # 使用序列化器处理分页数据
            items_serialized = schema_class(many=True).dump(paginated_query.items)
            response_data = {
                'items': items_serialized,
                'total': paginated_query.total,
                'page': paginated_query.page,
                'per_page': paginated_query.per_page,
                'has_next': paginated_query.has_next,
                'has_prev': paginated_query.has_prev,
            }
            return response_data
        return wrapper
    return decorator