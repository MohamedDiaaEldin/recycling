import os
from dotenv import load_dotenv

def get_value(key):        
    load_dotenv()
    jwt_secret = os.getenv(key)
    return jwt_secret