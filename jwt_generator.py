from cmath import exp
from flask import jsonify
import jwt





# generate jwt 
def encode_data(app, payload): ### public and email
    return  jwt.encode({"data": payload}, app.config['JWT_SECRET'], algorithm="HS256")


# decode jwt  
def decode_token(app , token):    
    return jwt.decode(str(token), app.config['JWT_SECRET'], algorithms='HS256')


# verify jwt 
def is_valid_jwt(app, jwt, public_id):
    try:
        payload = decode_token(app, jwt)
        return payload['data'] == public_id
    except:
        return False



