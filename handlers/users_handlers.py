import json
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from models import users
from flask import Blueprint, request, jsonify
from config import *
from models import crime
from libs import jwt, aws
from datetime import datetime, timedelta
from config import *


users_handlers = Blueprint('users_handlers', __name__)

def get_config():
    try:
        with open('config.json', 'r') as file:
            config_data = json.load(file)
            return config_data
    except Exception as e:
        print(f"Failed to read config.json: {e}")
        raise e


cfgFile = get_config()

@users_handlers.route('/configuration', methods=['GET'])
def get_config():
    try:
        return jsonify(cfgFile), 200
    except Exception as e:
        return jsonify({"message": "Failed to read configuration!"}), 500

@users_handlers.route('/', methods=['POST'])
def create_user():
    email = request.json['email']
    password = request.json['password']
    fcm_token = request.json['fcm_token']
    hashed_password = generate_password_hash(password)
    found_user = users.User.objects(email=email).first()
    if found_user:
        return jsonify({"message": "Email already exists!"}), 400

    notification_token = aws.storeLatestEndpointArn(fcm_token, 
                                             region_name=region_name, 
                                             access_key=aws_access_key_id, 
                                             secret_key=aws_secret_access_key,
                                             platform_application_arn=platform_application_arn)
    user = users.User(email=email, password=hashed_password, targetArn=notification_token)
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
    
def getTopCrimeIncidentList(longitude, latitude, distance_in_meters, start_date):
    nearby_incidents = crime.Incident.objects(
        location__near=[longitude, latitude],
        location__max_distance=distance_in_meters,
        occurred_at__gte=start_date  # Assuming the date field in your collection is named 'date'
    )
    
    return nearby_incidents

def getAreaRiskStatus(latitude, longitude, days=30, radius_km=1, threshold=1):
    """
    Check if a given location is a high-risk area based on past incidents within a specific timeframe.

    Parameters:
    - latitude, longitude: Coordinates of the location to check.
    - days: The number of past days to consider for incidents.
    - radius_km: The radius (in kilometers) to consider for nearby incidents.
    - threshold: The number of incidents within the radius to consider an area as high-risk.

    Returns:
    - 1 if the area is high-risk, 0 otherwise.
    """

    distance_in_meters = radius_km * 1000
    start_date = datetime.now() - timedelta(days=days)

    # Query for nearby incidents within the specified timeframe
    nearby_incidents = getTopCrimeIncidentList(longitude, latitude, distance_in_meters, start_date)

    count_incident = len(nearby_incidents)
    if count_incident >= threshold:
        # Convert the results to a list of dictionaries for JSON serialization
        incidents_list = [{"description": i.description, "location": i.location} for i in nearby_incidents]
        return True, incidents_list
    else:
        return False, []


@users_handlers.route('/location', methods=['POST'])
def update_location():
    currentLocation = request.json.get('currentLocation')
    userId = request.headers.get("Current-User-ID", "")
    if userId == "":
        return jsonify({"message": "Invalid userID"}), 401
    
    founderUser = users.User.objects(id=userId).first()
    if founderUser is None:
        return jsonify({"message": "User not exist"}), 404

    if currentLocation:
        cord = currentLocation.get("coordinates")
        if cord:
            # Update the user's currentLocation in the database
            isHighRisk, incidents_list = is_high_risk_area(cord[1], cord[0])
            if isHighRisk:
                aws.pushDataIntoNotificationAmazonSNS(incidents_list, 
                                           founderUser.targetArn, 
                                           "High Crime Alert", 
                                           region_name=region_name, 
                                           access_key=aws_access_key_id, 
                                           secret_key=aws_secret_access_key)
            users.User.objects(id=userId).update_one(set__currentLocation=cord)
            return jsonify({"message": "OK"})

    return jsonify({"message": "Invalid location data"}), 400