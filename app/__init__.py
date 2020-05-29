from flask import Flask, request
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app,db)
    #CORS(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

    from app.shop import bp as shop_bp
    app.register_blueprint(shop_bp)

    return app

from app import models