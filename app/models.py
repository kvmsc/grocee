from app import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.name)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    
class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(30), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    imgurl = db.Column(db.String(100))

    def __repr__(self):
        return '<Shop {}>'.format(self.name)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            'shop_id' : self.id,
            'name' : self.name,
            'image' : self.imgurl,
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    imgurl = db.Column(db.String(100))
    commodities = db.relationship('Commodity', 
                                backref='category', lazy=True)
    
    """
    brands = db.relationship('Brand',
                            backref='category', lazy=True)
    """

    def __repr__(self):
        return '<Category {}>'.format(self.name)
    
    def serialize(self):
        return {
            'cat_id' : self.id,
            'name' : self.name,
            'image' : self.imgurl,
        }


class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    sub_cat = db.Column(db.String(50), index=True)
    cat_id = db.Column(db.Integer, 
                        db.ForeignKey('category.id'), nullable=False)
    imgurl = db.Column(db.String(100))

    def __repr__(self):
        return '<Commodity {}>'.format(self.name)
    
    def serialize(self):
        return {
            'comm_id' : self.id,
            'name' : self.name,
            'image' : self.imgurl,
        }

"""
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cat_id = db.Column(db.Integer,
                        db.ForeignKey('category.id', nullable=False))

    def __repr__(self):
        return '<Brand {}>'.format(self.name)
"""
