from flask import Flask , jsonify , abort  , request , redirect
from flask_migrate import Migrate
from models import setup_db


app= Flask(__name__)
db = setup_db(app)
migrate  = Migrate(app=app, db=db)

@app.route("/")
def hello_world():
    # print()
    # customer = Customer.query.get(1)
    # return jsonify({
    #     'username' :customer.username ,
    #     'email' : customer.email
    # })    
    return 'iiiiiii'
