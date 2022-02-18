from flask import Flask , jsonify ,request
from flask_migrate import Migrate
from models import setup_db , Customer , Matrial, Category , MatrialCategory, WaitingCategory , SellOrder, SellCategorymatrial, Delivery
from flask_cors import CORS

app = Flask(__name__)
db = setup_db(app)
migrate  = Migrate(app=app, db=db)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

from error_handler import bad_request_handler, server_error_handler, success_request_handler, unauthorized_user_handler

@app.route('/customer', methods=['POST'])
def add_customer():
    body = request.get_json()
    if not Customer.is_valid_customer_data(body) :
        return bad_request_handler()
        
    try:
        ## create Customer 
        new_customer = Customer(name=body.get('name'), email=body.get('email'), password=body.get('password'), address=body.get('address'), points=0.0)
        db.session.add(new_customer)
        db.session.commit()     
        return success_request_handler()
    except:
        db.session.rollback()
        print('error while adding new customer')
        return server_error_handler()



@app.route('/login', methods=['POST'])
def login():
    body  = request.get_json() # extract json data 
    if not (Customer.is_valid_login_data(body)):
        return bad_request_handler()    
    try:        
        users = Customer.query.filter_by(email=body.get('email')).all() # query database
        if not Customer.is_valid_credentials(users, body):
                return unauthorized_user_handler()
        
        return success_request_handler()
    except:
        print('error while validating user')
        return server_error_handler()



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