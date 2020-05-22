from flask import jsonify, request, current_app, make_response, abort
from app.user import bp
from app.models import User, Shop
from app import db
import jwt 
import datetime
from helpers import *

#curl -i -H "Content-Type: application/json" -X POST -d '{"username":"admin", "password":"password"}' http://127.0.0.1:5000/api/login
@bp.route('/api/usr_login', methods = ['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(email=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'message' : 'Invalid Credentials!'}), 404
    
    token = jwt.encode({'id':user.id,'exp':datetime.datetime.utcnow() 
                        + datetime.timedelta(seconds=current_app.config['SESSION_TOKEN_EXPIRY'])},
                         current_app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')}), 200
    

@bp.route('/api/usr_register', methods = ['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    #if email exists
    user = User.query.filter_by(email=email).first()
    if not user is None:
        return jsonify({'message' : 'User already exists!'}), 403
    
    #add user to DB
    user = User(name=name,email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = jwt.encode({'id':user.id,'exp':datetime.datetime.utcnow() 
                        + datetime.timedelta(seconds=current_app.config['SESSION_TOKEN_EXPIRY'])},
                         current_app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')}), 200



