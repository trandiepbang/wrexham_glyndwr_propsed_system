from flask import Blueprint, request, jsonify
from models import users
from models import crime
from jwt import DecodeError, ExpiredSignatureError
from libs import jwt
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
    nearby_incidents_count = crime.Incident.objects(
        location__near=[longitude, latitude],
        location__max_distance=distance_in_meters,
        occurred_at__gte=start_date
    ).count()

    if nearby_incidents_count >= threshold:
        return 1  # High-risk area
    else:
        return 0  # Not a high-risk area


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