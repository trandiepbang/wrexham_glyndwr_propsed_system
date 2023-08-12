from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from libs import mongodb
from flask import Blueprint, request, jsonify

users_handlers = Blueprint('users_handlers', __name__)
dbCollection = mongodb.initMongoDB()
SECRET_KEY = os.environ.get('JWT_SECRETKEY', "!@#9012390123TRANDIEPBANGCUTIE" )


@users_handlers.route('/user', methods=['POST'])
def create_user():
    email = request.json['email']
    password = request.json['password']
    hashed_password = generate_password_hash(password)
    user = dbCollection['users'].find_one({'email': email})
    if user:
        return jsonify({"message": "Email already exists!"}), 400

    dbCollection['users'].insert_one({'email': email, 'password': hashed_password})
    return jsonify({"message": "User created successfully!"}), 201


@users_handlers.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    
    user = dbCollection['users'].find_one({'email': email})
    if not user:
        return jsonify({"message": "Email not found!"}), 404

    if check_password_hash(user['password'], password):
        token = jwt.PyJWT().encode(payload={'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=29)}, key = SECRET_KEY)
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Password is incorrect!"}), 401


@users_handlers.route('/forgot', methods=['POST'])
def forgot_password():
    # This is a basic implementation. In a real-world scenario, you'd send a reset link to the user's email.
    email = request.json['email']
    user = dbCollection['users'].find_one({'email': email})
    if not user:
        return jsonify({"message": "Email not found!"}), 404

    # For demonstration purposes, we're just sending back a message.
    return jsonify({"message": "Reset link sent to email!"})
