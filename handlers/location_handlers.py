from flask import Blueprint, request, jsonify

location_handlers = Blueprint('location_handlers', __name__)
@location_handlers.route('/', methods=['POST'])
def update_location():
    # This is a basic implementation. In a real-world scenario, you'd send a reset link to the user's email.
    currentLocation = request.json['currentLocation']
    if currentLocation != None:
        cord = currentLocation["coordinates"]
        
    return jsonify({"message": "Updated location"})
