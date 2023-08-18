from flask import Blueprint, request, jsonify
from models import users
from models import crime
from jwt import DecodeError, ExpiredSignatureError
from libs import jwt, aws
from datetime import datetime, timedelta

def is_high_risk_area(latitude, longitude, days=30, radius_km=1, threshold=10):
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
    nearby_incidents = crime.Incident.objects(
        location__near=[longitude, latitude],
        location__max_distance=distance_in_meters,
        occurred_at__gte=start_date  # Assuming the date field in your collection is named 'date'
    )

    count_incident = len(nearby_incidents)
    if count_incident >= threshold:
        # Convert the results to a list of dictionaries for JSON serialization
        incidents_list = [{"description": i.description, "location": i.location} for i in nearby_incidents]
        return True, incidents_list
    else:
        return False, []


location_handlers = Blueprint('location_handlers', __name__)
@location_handlers.route('/', methods=['POST'])
def update_location():
    token = request.headers.get('Authorization')  # Assuming the token is sent in the Authorization header
    if not token:
        return jsonify({"message": "Token is missing!"}), 401

    print("Token ", token)
    try:
        decoded_token = jwt.decode(token.replace("Bearer", ""))
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
            isHighRisk, incidents_list = is_high_risk_area(cord[1], cord[0])
            if isHighRisk:
                aws.send_push_notification(incidents_list[:10], "arn:aws:sns:ap-southeast-1:296809142595:crime-notification")
            users.User.objects(id=user_id).update_one(set__currentLocation=cord)
            return jsonify({"message": "OK"})

    return jsonify({"message": "Invalid location data"}), 400