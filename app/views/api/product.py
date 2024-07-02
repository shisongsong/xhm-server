from flask import Blueprint
from werkzeug.exceptions import NotFound
from flask_jwt_extended import jwt_required
from app.models.product import Product
from app.schemas.product import ProductSchema, product_schema
from app.views import api_view, paginator

api_product_bp = Blueprint('api_product', __name__, url_prefix='/api')

@api_product_bp.route('/products', methods=['GET'])
@jwt_required()
@api_view()
@paginator(ProductSchema)
def products_view():
    return Product.query.filter_by(deleted=False)

@api_product_bp.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
@api_view()
def product_view(product_id):
    product = Product.query.filter_by(deleted=False).get({"id": product_id})
    if not product:
        raise NotFound("产品不存在")
        
    product = product_schema.dump(product)
    return product