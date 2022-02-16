from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import Date, Float, String , Time
import json
Base = declarative_base()
DATABASE_URL='postgresql://mohamed:123@127.0.0.1:5432/recycling'
db = SQLAlchemy() ## ORM

def setup_db(app):
    print('database url ----->> ', DATABASE_URL)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db

def add(obj):
    db.session.add(obj)
    db.session.commit()
    
class Customer(db.Model):
    __tablename__ = 'customer'
    ## fields
    id = Column(Integer, primary_key=True) # outo increment
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    points = Column(Float, nullable=False)    
    buy_orders = relationship("BuyOrder")
    sell_orders = relationship("SellOrder")
    waiting = relationship("WaitingCategory")

    def __str__(self) :
        return f'{self.id}, {self.name}'

    def add(self):
        add(self)
    
class WaitingCategory(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    matrial_id = Column(Integer, ForeignKey('matrial.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))


    def add(self):
        add(self)

'''
NOTE  change to many  Deto many between SellOrder andlivery 
'''
class Delivery(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    orders = relationship("SellOrder")

    def add(self):
        add(self)



class SellOrder(db.Model):
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    delivery_id = Column(Integer, ForeignKey('delivery.id'))
    sell_orders = relationship("SellCategorymatrial")

    def add(self):
        add(self)


class BuyOrder(db.Model):
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    date = Column(Date, nullable=False) ## string for now
    time = Column(Time, nullable=False) ## String for now
    customer_id = Column(Integer, ForeignKey('customer.id')) 
    buy_orders = relationship("BuyCategoryMatrial")

    def add(self):
        add(self)

class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    matrialCategories = relationship("MatrialCategory")
    buy_orders = relationship("BuyCategoryMatrial")
    sell_orders = relationship("SellCategorymatrial")

    def get_category(self) :
        return {
            'id' : self.id, 
            'name' : self.name
        }
    def add(self):
        add(self)


class Matrial(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    matrialCategories = relationship("MatrialCategory")
    buy_orders = relationship("BuyCategoryMatrial")
    sell_orders = relationship("SellCategorymatrial")
    wating = relationship("WaitingCategory")

    def get_matrial(self) :
        return {
            'id' : self.id, 
            'name' : self.name
        }

    def add(self):
       add(self)

## Store
class MatrialCategory(db.Model):
    matrial_id = Column(Integer, ForeignKey('matrial.id'),  primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'),  primary_key=True)
    total_weight = Column(Float , nullable=False)
    km_price = Column(Float , nullable=False)
    km_points = Column(Float , nullable=False)

  
    def add(self):
        add(self)



class BuyCategoryMatrial(db.Model):
    matrial_id = Column(Integer,  ForeignKey('matrial.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), primary_key=True)
    buy_order_id = Column(Integer, ForeignKey('buy_order.id'), primary_key=True)
    weight = Column(Float, nullable=False)
    price =  Column(Float, nullable=False)
    

    def add(self):
        add(self)

class SellCategorymatrial(db.Model):
    matrial_id = Column(Integer, ForeignKey('matrial.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'),primary_key=True)
    sell_order_id = Column(Integer, ForeignKey('sell_order.id'), primary_key=True)
    weight = Column(Float, nullable=False)
    price =  Column(Float, nullable=False)  

    def add(self):
        add(self)