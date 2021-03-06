

from crypt import methods
from flask import Flask , jsonify ,request 
from flask_migrate import Migrate
from flask_cors import CORS
from models import Admin, setup_db , Customer , Matrial, Category , MatrialCategory , SellCategorymatrial, Delivery , Customer_OTP , PublicIdAuto, BuyCategoryMatrial, Zone
from otp import generateOTP
from message_email import send_email
import read_env
from jwt_generator import encode_data, is_valid_jwt 


app = Flask(__name__)
db = setup_db(app)
migrate  = Migrate(app=app, db=db)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['JWT_SECRET'] = read_env.get_value('JWT_SECRET')
from error_handler import bad_request_handler, server_error_handler, success_request_handler, unauthorized_user_handler, conflict_error_handler , succes_login_handler


## jwt and publlic id validation 
def is_valid_jwt_body(body):    
    return body and 'jwt' in body and 'public_id' in body


## /confirm_but request validation
def is_valid_buy_confirm(body):
    return body and 'weight' in body and body and 'matrial_id' in body and 'category_id' in body 


## /bur_order request validation 
def is_valid_buy_order_body(body):
    return body and 'weight' in body and body and 'matrial_id' in body and 'category_id' in body and "date" in body and 'time'  in body

# get delivery orders
def get_delivery_orders(orders):
    all_orders = []
    for order in orders:        
        if order.done == True:
            continue
        ## order data
        category_name = Category.query.get(order.category_id).name
        matrial_name = Matrial.query.get(order.matrial_id).name
        order_details = f'{matrial_name}-{category_name}'
        order_weight = order.weight
        ## customer data
        customer = Customer.query.get(order.customer_id)
        customer_name = f'{customer.first_name} {customer.last_name}'
        customer_phone = customer.phone
        customer_address = customer.address
        all_orders.append({
            'customer_name':customer_name,
            'customer_phone':customer_phone,
            'customer_address':customer_address,
            'order_weight':order_weight,
            'order_details':order_details,
            'date':order.date,
            'time':order.time,
            'id':order.id,
        })
        
    return all_orders

## validate confirm sell order body 
def is_valid_sell_confirm_body(body):
    return body and 'order_id' in body and 'weight' in body

#### ENDPOINTS


# get all active orders with total sell orders length
@app.route('/sell_active_orders', methods=['POST'])
def get_active_sell_orders():
    try:
        body = request.get_json()
        ## request body validation
        if not is_valid_jwt_body(body):
            return bad_request_handler()

        # get customer data
        admin = Admin.query.filter_by(id=int(body.get('public_id'))).first()        

        # jwt validation
        if  not admin or not  is_valid_jwt(app, body.get('jwt'), admin.email):
            return unauthorized_user_handler()

        sell_orders = SellCategorymatrial.query.all()
        all_counter = 0 
        active_orders = []

        for order in sell_orders:
            if order.done == True:
                all_counter  += 1 
                continue
            weight = order.weight
            time  =order.time
            date = order.date
            order_details = f'{ Category.query.get(order.category_id).name } - {Matrial.query.get(order.matrial_id).name }'            
            ## customer data
            customer = Customer.query.get(order.customer_id)
            customer_name = f'{customer.first_name} {customer.last_name}'
            customer_phone = customer.phone
            customer_location = customer.address
            ## get delivery data
            delivery = Delivery.query.get(order.delivery_id)
            delivery_name = delivery.name
            delivery_phone = delivery.phone
            delivery_number = delivery.id  
            data = {
                'customer_location':customer_location,
                'details':order_details,
                'weight':weight,
                'time':time,
                'date':date,
                'customer_name':customer_name,
                'customer_phone':customer_phone,
                'delivery_name':delivery_name,
                'delivery_phone':delivery_phone,
                'delivery_number':delivery_number
            }
            all_counter += 1 
            active_orders.append(data)
            
        return jsonify({
            "active_orders":active_orders,
            "length":all_counter
        })
    except:
        return server_error_handler()


## get all active buy orders with total buy orders length
@app.route('/buy_active_orders', methods=['POST'])
def get_active_buy_orders():
    try:
        body = request.get_json()
        ## request body validation
        if not is_valid_jwt_body(body):
            return bad_request_handler()

        # get customer data
        admin = Admin.query.filter_by(id=int(body.get('public_id'))).first()        

        # jwt validation
        if  not admin or not  is_valid_jwt(app, body.get('jwt'), admin.email):
            return unauthorized_user_handler()

        ## get all cuy orders 
        buy_orders = BuyCategoryMatrial.query.all()
        all_counter =  0
        active_orders = []
        for order in buy_orders:
            if order.done == True:
                all_counter += 1
                continue
                
            weight=order.weight
            price=order.price
            time=order.time
            date = order.date
            order_details = f'{ Category.query.get(order.category_id).name } - {Matrial.query.get(order.matrial_id).name }'            
            ## get customer data 
            customer = Customer.query.get(order.customer_id)
            customer_name = f'{customer.first_name} {customer.last_name}'
            customer_phone = customer.phone
            ## 
            data = {
                'weight':weight,                
                'price':price,            
                'time':time,            
                'date':date,            
                'details':order_details,            
                'customer_name':customer_name,            
                'customer_phone':customer_phone,            
            }            
            active_orders.append(data)
            all_counter += 1 
        
        return jsonify({
            'active_buy_orders':active_orders,
            'total_length':all_counter
        })
    except:
        return bad_request_handler()

@app.route('/customers')
def get_total_customers():
    try:
        customers = Customer.query.all()
        return jsonify({
            "status_code":200,
            "length":len(customers)
        })
    except:
        return bad_request_handler()

@app.route('/confirm_sell_order')
def confirm_sell_order():
    try:        
        otp = request.args.get('code')
        order_id = request.args.get('order_id')
        email = request.args.get('email')
        weight = request.args.get('weight')
        
        if otp == None or order_id == None or email==None or weight == None:
            return bad_request_handler()

        
        # get otp from database
        customer_otp = Customer_OTP.query.get(email)    
        ## if email not in database
        if customer_otp == None :            
            return unauthorized_user_handler()
        
        ## if not valid otp 
        if otp != customer_otp.otp:
            return unauthorized_user_handler()            

        # ## update old otp with new one 
        customer_otp.otp = generateOTP()
        customer_otp.commit_changes()
        
        # ## update order states to Done 
        sell_order = SellCategorymatrial.query.get(order_id)
        sell_order.done = True
        sell_order.weight = weight        
        sell_order.commit()
        
        # ## add new weight to database 
        category_matrial = MatrialCategory.query.filter_by(matrial_id=sell_order.matrial_id, category_id=sell_order.category_id).first() 
        category_matrial.total_weight += float(weight)
        category_matrial.commit()
        
        ## update total points 
        customer = Customer.query.get(sell_order.customer_id)
        
        points = int(weight) * int( category_matrial.km_points )
        ## update customer points
        customer.points += points
        customer.commit()
        
        # update sell order points
        sell_order.points = points
        sell_order.commit()
        
        
        return success_request_handler()
    except:
        return server_error_handler()


## confirm order detials and weight
@app.route('/confirm_sell', methods=['POST'])
def confirm_sell():
    try:
        body = request.get_json()
        if not is_valid_sell_confirm_body(body):
            return bad_request_handler()
        
        order_data = SellCategorymatrial.query.get(body.get('order_id'))
        order_details = f' { Category.query.get(order_data.category_id).name } - {Matrial.query.get(order_data.matrial_id).name }'
        customer_email = Customer.query.get(order_data.customer_id).email
        print(order_details)
        
        otp = generateOTP()
        # check if email in customer otp table 
        customer_otp = Customer_OTP.query.get(customer_email)    
        # if email is stored in database before 
        if customer_otp != None :
            # update otp with new one 
            customer_otp.otp = otp
            customer_otp.commit_changes()            
        else:
            # add OTP with email to database 
            customer = Customer_OTP(email=customer_email, otp=otp)        
            customer.add()
            
        send_email(customer_email, f"you order {order_details} = { body.get('weight') } km \n to confirm click this link http://localhost:5000/confirm_sell_order?code={otp}&order_id={order_data.id}&email={customer_email}&weight={body.get('weight') }", 'Confirm order')

        return success_request_handler()
    
    except:
        return server_error_handler()


# get all order with a delivery 
@app.route('/deliver_orders', methods=['POST'])
def deliver_orders():
    body  = request.get_json() 
    if not is_valid_jwt_body(body):
        return bad_request_handler()            
    try:                
        delivery = Delivery.query.filter_by(id=int(body.get('public_id'))).first()
        if not delivery or not  is_valid_jwt(app, body.get('jwt'), delivery.email):
            return unauthorized_user_handler()
            
        ## gell all order to a delivery 
        orders = SellCategorymatrial.query.filter_by(delivery_id=delivery.id).all()

        if len(orders) <= 0:
            return jsonify({
                "status_code":200,
                "message":"empty"
            })
      
        all_orders = get_delivery_orders(orders)
        return jsonify({
            'orders':all_orders,
            'status_code':200
        })   
    except:
        return server_error_handler()       


## delivery login
@app.route('/delivery_login', methods=['POST'])
def delivery_login():
    try:
        body = request.get_json()    
               
        if  not Customer.is_valid_login_data(body):
            return bad_request_handler()

        ## validate delivey 
        delivery = Delivery.query.filter_by(email=body.get('email')).first()
        if not delivery or delivery.password != body.get('password'): 
            return unauthorized_user_handler()
         
        # if valid user
        public_id = str(delivery.id)                
        # generate jwt with email
        jwt = encode_data(app , delivery.email)
        return succes_login_handler(jwt, public_id)
        
    except:
        return server_error_handler()
    
## admin login
@app.route('/admin_login', methods=['POST'])
def admin_login():
    try:
        body = request.get_json()    
               
        if  not Customer.is_valid_login_data(body):
            return bad_request_handler()

        ## validate delivey 
        delivery = Admin.query.filter_by(email=body.get('email')).first()
        if not delivery or delivery.password != body.get('password'): 
            return unauthorized_user_handler()
                 
        # if valid user
        public_id = str(delivery.id)                
        # generate jwt with email
        jwt = encode_data(app , delivery.email)
        return succes_login_handler(jwt, public_id)
        
    except:
        return server_error_handler()

        
## get all buy orders
## needs jwt and public_id
@app.route('/buy_orders', methods=['POST'])
def get_buy_orders():
    try:
        body = request.get_json()
        ## request body validation
        if not is_valid_jwt_body(body):
            return bad_request_handler()

        # get customer data
        customer = Customer.query.filter_by(public_id=int(body.get('public_id'))).first()        

        # jwt validation
        if  not customer or not  is_valid_jwt(app, body.get('jwt'), customer.email):
            return unauthorized_user_handler()
                
        # get all buy orders
        orders = BuyCategoryMatrial.get_orders(customer)        
        return jsonify({
            'status_code' : 200 ,            
            'orders':orders
        }), 200

    except:
        db.session.rollback()
        print('error while get sell order data')
        return server_error_handler()


### get all sell orders, active orders , points  
## needs jwt and public_id order_data
@app.route('/sell_orders', methods=['POST'])
def get_sell_orders():
    try:
        body = request.get_json()
        ## request body validation
        if not is_valid_jwt_body(body):
            return bad_request_handler()

        # get customer data
        customer = Customer.query.filter_by(public_id=int(body.get('public_id'))).first()        

        # jwt validation
        if  not customer or not  is_valid_jwt(app, body.get('jwt'), customer.email):
            return unauthorized_user_handler()
                
        # get all orders
        orders = SellCategorymatrial.get_orders(customer)        
        return jsonify({
            'status_code' : 200 ,
            'total_points' : customer.points,
            'orders':orders
        }), 200

    except:
        db.session.rollback()
        print('error while get sell order data')
        return server_error_handler()
        



### verify end point 
@app.route('/verify')
def verify_jwt():
    body  = request.get_json() 
    if not is_valid_jwt_body(body):
        return bad_request_handler()            
    try:                
        customer = Customer.query.filter_by(public_id=int(body.get('public_id'))).first()
        if customer and is_valid_jwt(app, body.get('jwt'), customer.email):
            return success_request_handler()
        else:        
            return unauthorized_user_handler()
    except:
        db.session.rollback()
        return server_error_handler()


## end point recives email and send OTP to email 
@app.route('/customer_email', methods=['POST'])
def otp():
    try:            
        body = request.get_json() 
        # request body validation 
    
        if not Customer_OTP.is_valid_request_data(body):
            return bad_request_handler()        
        email = body.get('email')

        # if email aleady siguned up 
        if Customer.is_email_there(email):            
            return conflict_error_handler()
        
        
        # generate OTP - one time password
        otp  = generateOTP()    

        # check if email in customer otp table 
        customer_otp = Customer_OTP.query.get(email)
        
        # if email is stored in database before 
        if customer_otp != None :
            # update otp with new one 
            customer_otp.otp = otp
            customer_otp.commit_changes()            
        else:
            # add OTP with email to database 
            customer = Customer_OTP(email=email, otp=otp)        
            customer.add()
                
        ## send email with otp
        send_email(to=email, message='OTP is ' + otp, subject='Bikya OTP')
        return success_request_handler()
    except : 
        print('error in otp generator end point')
        return server_error_handler()
  
## end point to verify OTP
## recives email and OTP
@app.route('/customer_otp', methods=['POST'])
def varify_otp():
    # compare OTP of the email address
    try:        
        body = request.get_json()
        if not Customer_OTP.is_valid_otp_request_data(body):
            return bad_request_handler()
        
        email = body.get('email')
        otp = body.get('otp')

        ## get otp from database
        customer_otp = Customer_OTP.query.get(email)
        
        ## if email not in database
        if customer_otp == None :            
            return unauthorized_user_handler()
        
        ## if not valid otp 
        if otp != customer_otp.otp:
            return unauthorized_user_handler()            

        ## update old otp with new one 
        customer_otp.otp = generateOTP()
        customer_otp.commit_changes()


        return success_request_handler()
    except:
        print('error while verify otp')
        return server_error_handler()

  
## ABDO 

### create new sell order 
## needs jwt and public_id order_data
@app.route('/sell_order', methods=['POST'])
def sell_order():
    try:
        body = request.get_json()        
        ## if there is no validation and sell order data
        if not is_valid_jwt_body(body) or not  SellCategorymatrial.is_valid_request_data(body):        
            return bad_request_handler()
        
        ## CHECK IF LOGIN OR NOT
        # get customer data where public_id = comming public_id
        customer = Customer.query.filter_by( public_id = int( body.get('public_id') ) ).first()
        # jwt validation
        if  not customer or not  is_valid_jwt(app, body.get('jwt'), customer.email):
            return unauthorized_user_handler()

        body  = body.get('sell_data')# get sell order data
        
        ## get km points 
        ## store 
        category_matrial = MatrialCategory.query.filter_by(matrial_id=body.get('matrial_id'), category_id=body.get('category_id')).first()        
        points = float(body.get('weight')) * category_matrial.km_points
        
        ## select dellivery for order
        selected_delivery = Delivery.query.filter_by(zone_id=int(body.get('zone_id'))).first()
    
        ## add sell order to database        
        ## INSERT
        sell_category_matrial = SellCategorymatrial(matrial_id=int(body.get('matrial_id')), category_id=int(body.get('category_id')) , delivery_id=selected_delivery.id, customer_id=customer.id, date=body.get('date'), time=body.get('time'), weight=float(body.get('weight')), points=points, done=False)
        sell_category_matrial.add()
    
        return success_request_handler()
    except:
        db.session.rollback()
        print('error while creating new sell order')
        return server_error_handler()


# get matrials from database 
# return matrials
@app.route('/matrials', methods=['GET'])
def get_matrial():
    try:        
        # select from Matrail table
        matrials = Matrial.query.all()     
            
        # convert into json 
        # return json 
        return Matrial.get_json_matrials(matrials)  
              
    except: # catch errors
        print('error geting matrials')
        return server_error_handler()
  
  
  
@app.route('/categories', methods=['GET'])
def get_categories():
    try:        
        # select from database
        categories = Category.query.all() 
      
        # convert into json 
        # return json 
        return Category.get_json_categories(categories)
        
    except: # catch errors
        print('error while getting categories')
        return server_error_handler
        
        
 
@app.route('/zones')
def get_zones():
    try:
        zones = Zone.query.all() 
        return Zone.get_json_zones(zones)
    except:
        return server_error_handler()


### ALI

## create buy order 
## confirm button
@app.route('/buy_order', methods=['POST'])
def buy_order():
    body = request.get_json()
    ## request body validation
    if not is_valid_jwt_body(body):
        return bad_request_handler()
    
    
    # get customer 
    # SELECT
    customer = Customer.query.filter_by(public_id=int(body.get('public_id'))).first()        
    # IF logied in 
    if  not customer or not  is_valid_jwt(app, body.get('jwt'), customer.email):
        return unauthorized_user_handler()
    ## check if valid confirm body 
    if not is_valid_buy_order_body(body):        
        return bad_request_handler()
    
    ## check if weight is found 
    wanted_weight  = body.get('weight')
    matrial_id  = body.get('matrial_id')
    category_id  = body.get('category_id')
    
    ## if weight is avaliable 
    category_matrial = MatrialCategory.query.filter_by(matrial_id=matrial_id ,  category_id=category_id).first()    
    ## if weight is not avaliable 
    if wanted_weight > category_matrial.total_weight :
        return jsonify({
            'message':'not found'            
        }), 404
        
    
    category_matrial = MatrialCategory.query.filter_by(matrial_id=body.get('matrial_id') ,  category_id=body.get('category_id')).first()    
    
    ## INSERT 
    ## add new buy order
    new_buy_order = BuyCategoryMatrial(matrial_id=body.get('matrial_id'), category_id=body.get('category_id'), customer_id=customer.id, date=body.get('date'), time=body.get('time'), weight=body.get('weight'), price=category_matrial.km_price * body.get('weight') , done=False)
    new_buy_order.add()    
    
    ## TODO make end point to reduce weight when client comes and take his order 
    # category_matrial.total_weight = category_matrial.total_weight - body.get('weight')
    # category_matrial.update()
    
    return jsonify({
        'status_code':200,
        "message":"success"
    })


## confirm weight 
## sumbit button
@app.route('/confirm_buy', methods=['POST'])
def confirm_buy():
    body = request.get_json()
    
    ## request body validation
    if not is_valid_jwt_body(body) or not is_valid_buy_confirm(body):
        return bad_request_handler()
            # get customer data
        
    
    ## SELECT
    ## login or not 
    customer = Customer.query.filter_by(public_id=int(body.get('public_id'))).first()        
    # jwt validation
    if  not customer or not  is_valid_jwt(app, body.get('jwt'), customer.email):
        return unauthorized_user_handler()

  
    wanted_weight  = body.get('weight')
    matrial_id  = body.get('matrial_id')
    category_id  = body.get('category_id')
    
    ## SELECT 
    ## weight
    category_matrial = MatrialCategory.query.filter_by(matrial_id=matrial_id ,  category_id=category_id).first()
    
    ## if weight is avaliable 
    if wanted_weight <= category_matrial.total_weight :        
        return jsonify({
            'status_code':200, 
            'price':category_matrial.km_price * wanted_weight,            
        })
    
    ## if weight is not avaliable
    return jsonify({
        'status_code':200,
        'message':'not found'        
    })





######## Gomaa

## create new customer
## add it to database
## sigin up
@app.route('/customer', methods=['POST'])
def add_customer():        
    try:
        # validate json request  formate 
        body = request.get_json()
        if not Customer.is_valid_customer_data(body) :
            return bad_request_handler()

        ## create new customer 
        public_id = PublicIdAuto.query.all()[0]        
        ## INSERT        
        new_customer = Customer(first_name=body.get('first_name'),last_name=body.get('last_name'), email=body.get('email'), password=body.get('password'), address=body.get('address'),phone=body.get('phone'), points=0.0, public_id=public_id.id+1)
        ## update public_id 
        public_id.id = public_id.id + 1
        # add to database
        new_customer.add()

        return success_request_handler()
        
    except:        
        db.session.rollback()
        print('error while adding new customer')
        return server_error_handler()

        
## get email and password
## validate user data
## return jwt 
@app.route('/login', methods=['POST'])
def login(): 
    try:        
        # validate json request  formate 
        body  = request.get_json() # extract json data     
        ## if email and password not in body
        if not (Customer.is_valid_login_data(body)):
            return bad_request_handler()    


        email = body.get('email') 
        # get user from database with this email   
        # SELECT            
        customer = Customer.query.filter_by(email=email).first()
        
        
        ##  if password is not correct 
        if not Customer.is_valid_credentials(customer, body):
            return unauthorized_user_handler()                                
                            
        # if valid user
        public_id = str(customer.public_id)        
        # generate jwt with email
        jwt = encode_data(app , email)
        return succes_login_handler(jwt, public_id)                
    except:
        db.session.rollback()
        print('error while validating user')        
        return server_error_handler()

        
        
if __name__ == '__main__':
    app.run()