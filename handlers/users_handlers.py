from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from models import users
from flask import Blueprint, request, jsonify
from libs import jwt

users_handlers = Blueprint('users_handlers', __name__)

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
        payload = {
            'user_id': str(found_user.id),  # Include user ID in the JWT payload
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=29)
        }
        token = jwt.encode(payload)
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Password is incorrect!"}), 401