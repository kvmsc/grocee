from app import db
from app.models import *

#add test user
u = User(name="admin", email="admin@grocery.com")
u.set_password("password")
db.session.add(u)

#adding shops
for i in range(1,21):
    s = Shop(name="Shop"+str(i), imgurl="https://bit.ly/3gpcSMI")
    db.session.add(s)

#adding categories
for i in range(1,7):
    c = Category(name="Category"+str(i),imgurl="https://bit.ly/36E0wfa")
    db.session.add(c)

from random import randint

#adding subcategories
for i in range(1,30):
    sc = Commodity(name="Subcat"+str(i), cat_id=randint(1,6))
    db.session.add(sc)

#adding brands
for i in range(1,30):
    b = Brand(name="Brand"+str(i), imgurl="https://bit.ly/3gjYkxG")
    db.session.add(b)

#adding brands in category
for i in range(1,7):
    c = Category.query.get(i)
    c.brands.append(Brand.query.get(i))
    c.brands.append(Brand.query.get(i*2))
    c.brands.append(Brand.query.get(i*3))
    c.brands.append(Brand.query.get(i*4))

#adding products
for i in range(100):
    p = Product(name="Product"+str(i),cat_id=randint(1,6), com_id=randint(1,29), brand_id=randint(1,29), imgurl="https://bit.ly/2X2PEUG")
    db.session.add(p)

#adding variants
for i in range(300):
    v = Variant(name="Variant"+str(i), prod_id=randint(1,99), qty="5g")
    db.session.add(v)

#adding shopvariants
for i in range(1,21):
    s = Shop.query.get(i)
    for j in range(i,i+260):
        v = Variant.query.get(j)
        pid = v.prod_id
        item = ShopVariant(shop_id=i,item_id=j,prod_id=pid,price=0.0)
        s.items.append(item)

