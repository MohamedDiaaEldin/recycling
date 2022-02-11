from os import pipe
from flask import Flask , jsonify , abort  , request , redirect , render_template
from flask_migrate import Migrate
from models import setup_db , Customer
from flask_cors import CORS


app = Flask(__name__)
db = setup_db(app)
migrate  = Migrate(app=app, db=db)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


# @app.route("/")
# def hello_world():    
#     return jsonify({
#         'name':'ali',
#         'age':20
#     })



def is_valid_user_data(body):
    return not (body != None and 'name' not in body or 'email' not in body or 'password' not in body or 'address' not in body)


@app.route('/customer', methods=['POST'])
def add_customer():
    body = request.get_json()
    
    if not is_valid_user_data(body):
        return jsonify({
            'sucess':False,
            'status_code' : 400 ,
            'message': 'bad request'
        }) 

    try:
        ## create Customer 
        new_customer = Customer(name=body.get('name'), email=body.get('email'), password=body.get('password'), address=body.get('address'), points=0.0)
        db.session.add(new_customer)
        db.session.commit()            
        return jsonify({
            'status_code' :200 ,
            'success': True
        })
    except:
        db.session.rollback()
        print('error while adding new customer')
        return jsonify({
            'status_code': 500 ,
            'message':'server error'
        })
        


def is_valid_login_data(body):
    return not (body == None or 'email' not in body or 'password' not in body)

@app.route('/login', methods=['POST'])

def login():
    body  = request.get_json()
    if not (is_valid_login_data(body)):
        return jsonify({
            'success' : False,
            'status_code':400,
            'message' : "server error",            
        })
    try:
        users = Customer.query.filter_by(email=body.get('email')).all()   ## select from database     
        
        if len(users) == 0 or users[0].password != body.get('password'):
            return jsonify({
                'success' : False,
                'status_sode': 401,
                'message' :' unauthorized user'
            })
            
        return jsonify({
            'success': True,
            'status_code' : 200
        })
    except:
        print('error while validating user')
        return jsonify({
            'status_code': 500 ,
            'message':'server error'
        })