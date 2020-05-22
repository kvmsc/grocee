from flask import jsonify, request, current_app, make_response, abort
from app.user import bp
from app.models import Shop
from app import db
import jwt 
import datetime
from helpers import *

#curl -i -H "Content-Type: application/json" -X POST -d '{"username":"admin", "password":"password"}' http://127.0.0.1:5000/api/login
@bp.route('/api/shop_login', methods = ['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    shop = Shop.query.filter_by(email=username).first()
    if shop is None or not shop.check_password(password):
        return jsonify({'message' : 'Invalid Credentials!'}), 400
    
    token = jwt.encode({'id':shop.id,'exp':datetime.datetime.utcnow() 
                        + datetime.timedelta(seconds=current_app.config['SESSION_TOKEN_EXPIRY'])},
                         current_app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')}), 200
    

@bp.route('/api/shop_register', methods = ['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    #if email exists
    shop = Shop.query.filter_by(email=email).first()
    if not shop is None:
        return jsonify({'message' : 'User already exists!'}), 400
    
    #add user to DB
    shoop = Shop(name=name,email=email)
    shop.set_password(password)
    db.session.add(shop)
    db.session.commit()

    token = jwt.encode({'id':shop.id,'exp':datetime.datetime.utcnow() 
                        + datetime.timedelta(seconds=current_app.config['SESSION_TOKEN_EXPIRY'])},
                         current_app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')}), 200
