import jwt

# generate jwt 
### payload email
def encode_data(app, payload): 
    return  jwt.encode({"data": payload}, app.config['JWT_SECRET'], algorithm="HS256")


# decode jwt  
# decoded email token 
def decode_token(app , token):    
    return jwt.decode(token, app.config['JWT_SECRET'], algorithms='HS256')


# verify jwt 
def is_valid_jwt(app, jwt, email):
    try:
        payload = decode_token(app, jwt)
        return payload['data'] == email
    except:
        return False

