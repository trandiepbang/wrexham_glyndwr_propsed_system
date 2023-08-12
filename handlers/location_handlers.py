from flask import Blueprint, request, jsonify
from models import users
from jwt import DecodeError, ExpiredSignatureError
from libs import jwt
import os
SECRET_KEY = os.environ.get('JWT_SECRETKEY', "!@#9012390123TRANDIEPBANGCUTIE" )

location_handlers = Blueprint('location_handlers', __name__)
@location_handlers.route('/', methods=['POST'])
def update_location():
    token = request.headers.get('Authorization')  # Assuming the token is sent in the Authorization header
    if not token:
        return jsonify({"message": "Token is missing!"}), 401

    try:
        decoded_token = jwt.decode(token)
        user_id = decoded_token['user_id']
    except DecodeError:
        return jsonify({"message": "Invalid token!"}), 401
    except ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401

    currentLocation = request.json.get('currentLocation')
    if currentLocation:
        cord = currentLocation.get("coordinates")
        if cord:
            # Update the user's currentLocation in the database
            users.User.objects(id=user_id).update_one(set__currentLocation=currentLocation)
            return jsonify({"message": "OK"})

    return jsonify({"message": "Invalid location data"}), 400