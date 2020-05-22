from flask import request, current_app, jsonify
from app.main import bp
from app.models import Shop, User
import jwt
from helpers import *

@bp.route('/')
def index():
    return "You've reached Grocee API"

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
