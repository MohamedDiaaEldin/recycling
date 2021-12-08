from enum import Flag
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.sqltypes import Date, Float, String , Time
Base = declarative_base()

DATABASE_URL='postgresql://mohamed:123@127.0.0.1:5432/recycling'
db = SQLAlchemy()
def setup_db(app):
    print('database url ----->> ', DATABASE_URL)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db

# class Department(db.Model):    
#     __tablename__ = 'department'
#     id = Column(Integer, primary_key=True)
#     customers = relationship("Employee")

# class Employee(db.Model):
#     id = Column(Integer, primary_key=True)
#     username = Column(String, nullable=False)
#     department_id = Column(Integer, ForeignKey('department.id'))


class Customer(db.Model):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    points = Column(Float, nullable=False)
    buy_orders = relationship("BuyOrder")
    sell_orders = relationship("SellOrder")
    waiting = relationship("WaitingCategory")
    
class WaitingCategory(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    matrial_id = Column(Integer, ForeignKey('matrial.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
'''
NOTE 
change to many to many between SellOrder and Delivery 
'''
class Delivery(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    orders = relationship("SellOrder")


class SellOrder(db.Model):
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    delivery_id = Column(Integer, ForeignKey('delivery.id'))
    sell_orders = relationship("SellCategorymatrial")

class BuyOrder(db.Model):
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    date = Column(Date, nullable=False) ## string for now
    time = Column(Time, nullable=False) ## String for now
    customer_id = Column(Integer, ForeignKey('customer.id'))
    buy_orders = relationship("BuyCategoryMatrial")


class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    matrialCategories = relationship("MatrialCategory")
    buy_orders = relationship("BuyCategoryMatrial")
    sell_orders = relationship("SellCategorymatrial")
    


class Matrial(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    matrialCategories = relationship("MatrialCategory")
    buy_orders = relationship("BuyCategoryMatrial")
    sell_orders = relationship("SellCategorymatrial")
    wating = relationship("WaitingCategory")

    


## Store
class MatrialCategory(db.Model):
    id = Column(Integer, primary_key=True)
    total_weight = Column(Float , nullable=False)
    km_price = Column(Float , nullable=False)
    km_points = Column(Float , nullable=False)

    matrial_id = Column(Integer, ForeignKey('matrial.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

class BuyCategoryMatrial(db.Model):
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    price =  Column(Float, nullable=False)

    matrial_id = Column(Integer, ForeignKey('matrial.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    buy_order_id = Column(Integer, ForeignKey('buy_order.id'))

class SellCategorymatrial(db.Model):
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    price =  Column(Float, nullable=False)

    matrial_id = Column(Integer, ForeignKey('matrial.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    sell_order_id = Column(Integer, ForeignKey('sell_order.id'))