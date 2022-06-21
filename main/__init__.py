from flask import Flask , jsonify ,request 
from flask_migrate import Migrate
from flask_cors import CORS
from models import setup_db , Customer , Matrial, Category , MatrialCategory, WaitingCategory , SellCategorymatrial, Delivery , Customer_OTP , PublicIdAuto, BuyCategoryMatrial
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



@app.route('/')
def index():
    return 'hi'



def is_valid_jwt_body(body):
    return body and 'jwt' in body and 'public_id' in body




def is_valid_buy_confirm(body):
    return body and 'weight' in body and body and 'matrial_id' in body and 'category_id' in body 

def is_valid_buy_order_body(body):
    return body and 'weight' in body and body and 'matrial_id' in body and 'category_id' in body and "date" in body and 'time'  in body

'''

public_id 
weight 
jwt
categoy_id
matrial_id 
date 
time
''' 

@app.route('/buy_order', methods=['POST'])
def buy_order():
    body = request.get_json()
    ## request body validation
    if not is_valid_jwt_body(body):
        return bad_request_handler()
            # get customer data
    customer = Customer.query.filter_by(public_id=int(body.get('public_id'))).first()        

    # jwt validation
    if  not customer or not  is_valid_jwt(app, body.get('jwt'), customer.email):
        return unauthorized_user_handler()

    ## check if valid confirm body 
    if not is_valid_buy_order_body(body):        
        return bad_request_handler()
    
    category_matrial = MatrialCategory.query.filter_by(matrial_id=body.get('matrial_id') ,  category_id=body.get('category_id')).first()    
    new_buy_order = BuyCategoryMatrial(matrial_id=body.get('matrial_id'), category_id=body.get('category_id'), customer_id=customer.id, date=body.get('date'), time=body.get('time'), weight=body.get('weight'), price=category_matrial.km_price * body.get('weight') , done=False)
    new_buy_order.add()    
    
    category_matrial.total_weight = category_matrial.total_weight - body.get('weight')
    category_matrial.update()
    
    return jsonify({
        'status_code':200,
        "message":"success"
    })



@app.route('/confirm_buy', methods=['POST'])
def confirm_buy():
    body = request.get_json()
    ## request body validation
    if not is_valid_jwt_body(body):
        return bad_request_handler()
            # get customer data
    customer = Customer.query.filter_by(public_id=int(body.get('public_id'))).first()        

    # jwt validation
    if  not customer or not  is_valid_jwt(app, body.get('jwt'), customer.email):
        return unauthorized_user_handler()

    ## check if valid confirm body 
    if not is_valid_buy_confirm(body):
        return bad_request_handler()
    
    wanted_weight  = body.get('weight')
    matrial_id  = body.get('matrial_id')
    category_id  = body.get('category_id')
    
    category_matrial = MatrialCategory.query.filter_by(matrial_id=matrial_id ,  category_id=category_id).first()
    
    ## if weight is avaliable 
    if wanted_weight <= category_matrial.total_weight :
        return jsonify({
            'status_code':200, 
            'price':category_matrial.km_price * wanted_weight,            
        })
    
    ## if wait not avaliable
    return jsonify({
        'status_code':200,
        'message':'not found'        
    })


        
    
    # for d in data :
    #     print(d.category_id)
    #     print(d.matrial_id)
    #     print(d.km_price)
    #     print(d.total_weight)
    #     print(d.km_points)
    #     print('')
    
    
    return "ok"



### end point to get  all orders, active orders , points  
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
        

### end point to create new sell order 
## needs jwt and public_id order_data

@app.route('/sell_order', methods=['POST'])
def sell_order():
    try:
        body = request.get_json()
        if not is_valid_jwt_body(body) or not  SellCategorymatrial.is_valid_request_date(body):
            return bad_request_handler()
        
        # get customer data
        customer = Customer.query.filter_by(public_id=int(body.get('public_id'))).first()        

        # jwt validation
        if  not customer or not  is_valid_jwt(app, body.get('jwt'), customer.email):
            return unauthorized_user_handler()

        body  = body.get('sell_data')

        # ## calculate points depneds on store  TODO 
        # ## dummy calulations 
        
        points = float(body.get('weight')) * 2.5        
        # # ## add to database
        # print(points)
        sell_category_matrial = SellCategorymatrial(matrial_id=int(body.get('matrial_id')), category_id=int(body.get('category_id')) , delivery_id=1, customer_id=customer.id, date=body.get('date'), time=body.get('time'), weight=float(body.get('weight')), points=points, done=False)
        sell_category_matrial.add()

        
        return success_request_handler()
    except:
        db.session.rollback()
        print('error while creating new sell order')
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
    # try:            
    body = request.get_json() 
    # request body validation 
    print('-------------------->', body)
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
    # except : 
    #     print('error in otp generator end point')
    #     return server_error_handler()
    




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
    



## create new customer
## add it to database
@app.route('/customer', methods=['POST'])
def add_customer():        
    try:
        # validate json request  formate 

        body = request.get_json()
        if not Customer.is_valid_customer_data(body) :
            return bad_request_handler()

        ## create new customer 
        public_id = PublicIdAuto.query.all()[0]
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
        if not (Customer.is_valid_login_data(body)):
            return bad_request_handler()    

        email = body.get('email') 

        # get user from database with this email                
        customer = Customer.query.filter_by(email=email).first()
        ##  valid not valid user 
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

# get matrials from database 
# return matrials
@app.route('/matrials', methods=['GET'])
def get_matrial():
    try:        
        matrials = Matrial.query.all() # query database
        return Matrial.get_json_matrials(matrials)
    except:
        print('error geting matrials')
        return server_error_handler()
  

@app.route('/categories', methods=['GET'])
def get_categories():
    try:        
        categories = Category.query.all() # query database
        return Category.get_json_categories(categories)
    except:
        print('error while getting categories')
        return server_error_handler
        

        
if __name__ == '__main__':
    app.run()