from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from libs import mongodb
from models import users
from flask import Blueprint, request, jsonify

users_handlers = Blueprint('users_handlers', __name__)
SECRET_KEY = os.environ.get('JWT_SECRETKEY', "!@#9012390123TRANDIEPBANGCUTIE" )

mongodb.initMongoDB()



@users_handlers.route('/user', methods=['POST'])
def create_user():
    email = request.json['email']
    password = request.json['password']
    hashed_password = generate_password_hash(password)
    found_user = users.User.objects(email=email).first()
    if found_user:
        return jsonify({"message": "Email already exists!"}), 400

    user = users.User(email=email, password=hashed_password)
    user.save()

    return jsonify({"message": "User created successfully!"}), 201


@users_handlers.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    
    found_user = users.User.objects(email=email).first()
    if not found_user:
        return jsonify({"message": "Email not found!"}), 404

    if check_password_hash(found_user['password'], password):
        token = jwt.PyJWT().encode(payload={'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=29)}, key = SECRET_KEY)
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Password is incorrect!"}), 401


@users_handlers.route('/forgot', methods=['POST'])
def forgot_password():
    # This is a basic implementation. In a real-world scenario, you'd send a reset link to the user's email.
    email = request.json['email']
    found_user = users.User.objects(email=email).first()
    if not found_user:
        return jsonify({"message": "Email not found!"}), 404

    # For demonstration purposes, we're just sending back a message.
    return jsonify({"message": "Reset link sent to email!"})
