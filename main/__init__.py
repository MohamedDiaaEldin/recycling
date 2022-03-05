from asyncio import constants
import email
from wsgiref.util import request_uri
from flask import Flask , jsonify ,request 
from flask_migrate import Migrate
from flask_cors import CORS
from models import setup_db , Customer , Matrial, Category , MatrialCategory, WaitingCategory , SellCategorymatrial, Delivery , Customer_OTP , PublicIdAuto
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




### end point to get  all orders, active orders , points  
## needs jwt and public_id order_data


### end point to create new sell order 
## needs jwt and public_id order_data



### verify end point 
@app.route('/verify')
def verify_jwt():
    body  = request.get_json() 
    if body == None or 'jwt' not in body or 'public_id' not in body:
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
        
        
        # generate OTP - oen time password
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