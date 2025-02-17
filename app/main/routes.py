from flask import request, current_app, jsonify
from app.main import bp
from app import db
from app.models import Shop, User, Category, Commodity, Brand, Product, ShopVariant
import jwt
from helpers import *

@bp.route('/')
def index():
    return "<html><body><h1>You've reached Grocee API</h1></body></html>"

@bp.route('/api', methods=['POST'])
@token_required
def api():
    return jsonify({'message':'You reached protected resource'}), 200

@bp.route('/api/get_shops', methods=['POST'])
@token_required
def get_shops():
    #use token to get user_id and his location

    #use page argument for paginaton
    page = int(request.json.get('page'))
    shops = Shop.query.paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    return jsonify(shops=[s.serialize() for s in shops.items], has_next=shops.has_next), 200


@bp.route('/api/get_categories', methods=['POST'])
@token_required
def get_categories():
    categories = Category.query.all()
    return jsonify(categories=[c.serialize() for c in categories]), 200


@bp.route('/api/get_items', methods=['POST'])
@token_required
def get_items():
    
    shop_id = int(request.json.get('shop_id'))
    if not shop_id:
        return jsonify(message="Shop ID not found."), 400
    
    prod_query = db.session.query(Product)

    cat_id = request.json.get('cat_id')
    if cat_id:
        cat_id = int(cat_id)
        prod_query.filter(Product.cat_id==cat_id)

    brand_id = request.json.get('brands')
    if brand_id:
        brand_id = int(brand_id)
        prod_query.filter(Product.brand_id==brand_id)
    
    subcat_id = request.json.get('subcat_id')
    if subcat_id:
        subcat_id = int(subcat_id)
        prod_query.filter(Product.com_id==subcat_id)
    
    prod_query.join(ShopVariant).filter(ShopVariant.shop_id==shop_id).distinct()

    page = int(request.json.get('page'))

    products = prod_query.paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    
    return jsonify(products=[p.serialize(shop_id) for p in products.items],
                     has_next=products.has_next), 200                     

