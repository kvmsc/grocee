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
 
    items = db.relationship('ShopVariant', 
                            backref=db.backref('shop', lazy=True), 
                            lazy='dynamic')

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


#auxillary table for brand & category relationship
brand_category = db.Table('brand_category',
    db.Column('brand_id', db.Integer, db.ForeignKey('brand.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    imgurl = db.Column(db.String(100))
    
    commodities = db.relationship('Commodity', 
                                backref='category', lazy=True)
    brands = db.relationship('Brand', secondary=brand_category, lazy='joined',
                            backref=db.backref('categories', lazy=True))
    products = db.relationship('Product', 
                            backref='category', lazy=True)
    def __repr__(self):
        return '<Category {}>'.format(self.name)
    
    def serialize(self):
        return {
            'cat_id' : self.id,
            'name' : self.name,
            'image' : self.imgurl,
        }

#SUBCATEGORY TABLE
class Commodity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cat_id = db.Column(db.Integer, 
                        db.ForeignKey('category.id'), nullable=False)
    
    products = db.relationship('Product',
                            backref='commodity', lazy=True)
    #also Has "category" backref to return the Category object

    def __repr__(self):
        return '<Commodity {}>'.format(self.name)
    
    def serialize(self):
        return {
            'comm_id' : self.id,
            'name' : self.name,
        }

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    imgurl = db.Column(db.String(100))

    products = db.relationship('Product',
                            backref='brand', lazy=True)
    def serialize(self):
        return {
            'brand_id' : self.id,
            'name' : self.name,
            'image' : self.imgurl,
        }

    def __repr__(self):
        return '<Brand {}>'.format(self.name)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cat_id = db.Column(db.Integer, 
                        db.ForeignKey('category.id'), nullable=False)
    com_id = db.Column(db.Integer, 
                        db.ForeignKey('commodity.id'), nullable=False)
    brand_id = db.Column(db.Integer, 
                        db.ForeignKey('brand.id'))
    imgurl = db.Column(db.String(50))

    variants = db.relationship('Variant',
                            backref='product', lazy=True)

    def __repr__(self):
        return '<Product {}>'.format(self.name)
    
    def serialize(self, shop_id):
        return {
            "prod_id" : self.id,
            "name" : self.name,
            "image" : self.imgurl,
            "variants" : [_ for _ in (v.serialize(shop_id) for v in self.variants) if _ is not None],
        }
    
class Variant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    prod_id = db.Column(db.Integer,
                        db.ForeignKey('product.id'), nullable=False)
    qty = db.Column(db.String(20))

    def __repr__(self):
        return '<Variant {}>'.format(self.name)    
    
    def serialize(self, shop_id):
        _sv = db.session.query(ShopVariant).get((shop_id,self.id))
        if not _sv:
            return None
        return {
            "var_id" : self.id,
            "qty" : self.qty,
            "price" : _sv.price,
        }

class ShopVariant(db.Model):
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('variant.id'), primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'), index=True, nullable=False)
    price = db.Column(db.Float)

    
