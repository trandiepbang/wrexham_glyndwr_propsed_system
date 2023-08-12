import os
import jwt

SECRET_KEY = os.environ.get('JWT_SECRETKEY', "!@#9012390123TRANDIEPBANGCUTIE" )
def decode(token):
   return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

def encode(payload):
   return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
