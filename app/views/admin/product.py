from flask import Blueprint, request, current_app
from werkzeug.exceptions import BadRequest, NotFound
from flask_jwt_extended import jwt_required
from app.controllers.admin.product_controller import create, update
from app.jwt_required import admin_route_required
from app.models.product import Product
from app.schemas.product import ProductSchema, products_schema, product_schema
from app.views import api_view, paginator

admin_product_bp = Blueprint('admin_product', __name__, url_prefix='/admin')

@admin_product_bp.route('/products', methods=['GET'])
@jwt_required()
@admin_route_required
@api_view()
@paginator(ProductSchema)
def products_view():
    return Product.query

@admin_product_bp.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
@admin_route_required
@api_view()
def product_view(product_id):
    product = Product.query.get({"id": product_id})
    if not product:
        raise NotFound("产品不存在")
        
    product = product_schema.dump(product)
    return product

@admin_product_bp.route('/products', methods=['POST'])
@jwt_required()
@admin_route_required
@api_view()
def create_view():
    json_data = request.get_json()
    if not json_data:
        raise BadRequest("缺少必要参数")

    errors = create(json_data)
    return not errors, {"errors": errors}, 200
    
@admin_product_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
@admin_route_required
@api_view()
def update_view(product_id):
    json_data = request.get_json()
    if not json_data or not product_id:
        raise BadRequest("缺少必要参数")

    errors = update(product_id, json_data)
    return not errors, {"errors": errors}, 200