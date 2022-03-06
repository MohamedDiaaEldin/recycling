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
    def is_valid_credentials(user, body):
        return user and user.password == body.get('password')
    @staticmethod
    def is_valid_login_data(body):
        return body and 'email'  in body and 'password'  in body
    @staticmethod
    def is_valid_customer_data(body):
        return  body  and 'first_name' in body and 'last_name'  in body and 'email' in body and 'password' in body and 'address' in body and 'phone' in body
    def __str__(self) :
        return f'< id:{self.id}, email:{self.email}>'

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
            'length': len(list),
            'status_code':200
            }), 200

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
            'length': len(list),
            'status_code':200
        }), 200
        
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


    @staticmethod
    def is_valid_request_date(body):
        if body and 'sell_data' in body:
            body = body.get('sell_data')
            return 'category_id' in body and 'matrial_id' in body and 'date' in body and 'time' in body and 'weight' in body
        return False

    @staticmethod
    def get_orders(customer):
        sell_orders = SellCategorymatrial.query.filter_by(customer_id=customer.id).all()
        all_orders = []
        for sell_order in sell_orders:    
            category = Category.query.get(sell_order.category_id)            
            matrial = Matrial.query.get(sell_order.matrial_id)            
            order_details = f"{category.name} - {matrial.name}"                
            order_data = {
                'date' : sell_order.date,
                'time' : sell_order.time,
                'weight' : sell_order.weight,
                'points' : sell_order.points,
                'order_detials' : order_details,
                'done' : sell_order.done
            }             
            all_orders.append(order_data)
        return all_orders

    def add(self):
        add(self)


## for autoincrment 
class PublicIdAuto(db.Model):
    id = Column(Integer, primary_key=True)

    def add(self):        
        add(self)


