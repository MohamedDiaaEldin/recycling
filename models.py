from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  Column, Integer, ForeignKey, false
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Date, Float, String , Time , Boolean
from flask import jsonify


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



class Customer_OTP(db.Model):
    __tablename__ = 'customer_otp'
    email = Column(String, primary_key=True)
    otp = Column(String, nullable=False)

    def add(self):
        add(self)

    def commit_changes(self):
        db.session.commit()

    @staticmethod
    def is_valid_request_data(body):
        return body != None and 'email' in body 

    @staticmethod
    def is_valid_otp_request_data(body):
        return body != None and 'email' in body and 'otp' in body 



class Customer(db.Model):
    __tablename__ = 'customer'
    ## fields
    id = Column(Integer, primary_key=True) # outo increment    
    public_id = Column(Integer) # outo increment    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    points = Column(Float, nullable=False)    
    waiting = relationship("WaitingCategory")
    

    @staticmethod
    def is_email_there(email):
        ## check if user is signed up before 
        customers = Customer.query.filter_by(email=email).all()
        if len(customers) == 0 :
            return False
        return True             


    @staticmethod
    def is_valid_credentials(users, body):
        return not (len(users) == 0 or users[0].password != body.get('password'))
    @staticmethod
    def is_valid_login_data(body):
        return not (body == None or 'email' not in body or 'password' not in body)
    @staticmethod
    def is_valid_customer_data(body):
        return not (body != None and 'first_name' not in body or 'last_name' not in body or 'email' not in body or 'password' not in body or 'address' not in body or 'phone' not in body)
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

    def add(self):
        add(self)


# for delivery page - needs admin
# class SellOrder(db.Model):
#     id = Column(Integer, primary_key=True)    
#     sell_category_matrial_id = Column(Integer, ForeignKey('sell_categorymatrial.id'))
#     delivery_id = Column(Integer, ForeignKey('delivery.id'))    

#     def add(self):
#         add(self)


# class BuyOrder(db.Model):
#     id = Column(Integer, primary_key=True)            
#     buy_category_matrial = Column(Integer, ForeignKey('buy_category_matrial.id')) 

#     def add(self):
#         add(self)

class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    matrialCategories = relationship("MatrialCategory")
    
    @staticmethod
    def get_json_categories(categories):
        list = []
        for category in categories:
            list.append(category.get_category())    
        return jsonify({
            'categories' : list, 
            'length': len(list)
            })

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

    @staticmethod
    def get_json_matrials(matrials):
        list = []
        for matrial in matrials:
            list.append(matrial.get_matrial())            
        return jsonify({
            'matrials' : list, 
            'length': len(list)
        })
        
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
    id = Column(Integer, primary_key=True)
    matrial_id = Column(Integer,  ForeignKey('matrial.id'))
    category_id = Column(Integer, ForeignKey('category.id'))        
    customer_id = Column(Integer, ForeignKey('customer.id'))            
    date = Column(String, nullable=False) 
    time = Column(String, nullable=False) 
    weight = Column(Float, nullable=False)
    price =  Column(Float, nullable=False)
    done =  Column(Boolean, nullable=False)
 

    def add(self):
        add(self)

class SellCategorymatrial(db.Model):    
    id = Column(Integer, primary_key=True)
    matrial_id = Column(Integer, ForeignKey('matrial.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    delivery_id = Column(Integer, ForeignKey('delivery.id'))
    customer_id = Column(Integer, ForeignKey('customer.id')) # will start with default untill admin select whihc delivery
    date = Column(String, nullable=False) 
    time = Column(String, nullable=False) 
    weight = Column(Float, nullable=False)
    points =  Column(Float, nullable=False)  # default false 
    done =  Column(Boolean, nullable=False)

    def add(self):
        add(self)


## for autoincrment 
class PublicIdAuto(db.Model):
    id = Column(Integer, primary_key=True)

    def add(self):        
        add(self)


