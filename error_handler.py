
  
from flask import jsonify
from main import app


@app.errorhandler(400)
def bad_request_handler(message='bad request'):
        return jsonify({
            'success' : False,
            'status_code':400,
            'message' : message,            
        }), 400


@app.errorhandler(500)
def server_error_handler(message='server error'):
        return jsonify({
            'status_code': 500 ,
            'message':message
        }), 500

@app.errorhandler(409)
def conflict_error_handler(message='Email Conflict'):
        return jsonify({
            'status_code': 409 ,
            'message':message
        }), 409


@app.errorhandler(401)
def  unauthorized_user_handler(message='unauthorized user'):
    return jsonify({
        'success' : False,
        'status_sode': 401,
        'message' :message
    }), 401




def succes_login_handler(jwt, public_id):
    return jsonify({
        'status_code': 200,
        'success' : True , 
        'jwt' : jwt,
        'public_id' : public_id,
    }), 200

def success_request_handler():
        return jsonify({
            'status_code' :200,
            'success': True
        }) , 200
        