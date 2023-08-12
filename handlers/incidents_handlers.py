from flask import Blueprint, request, jsonify
from models import crime

incident_handlers = Blueprint('incident_handlers', __name__)
@incident_handlers.route('/', methods=['POST'])
def create_incident():
    data = request.json
    description = data.get('description')
    incident_type = data.get('incident_type')
    summary = data.get('summary')
    location = data.get('location')
    occurred_at = data.get('occurred_at')
    source = data.get('source')

    # Validate the data (you can add more validation as needed)
    if not all([description, incident_type, summary, location, occurred_at]):
        return jsonify({"message": "All fields are required!"}), 400

    incident = crime.Incident(
        description=description,
        incident_type=incident_type,
        summary=summary,
        location=location,
        occurred_at=occurred_at,
        source=source
    )
    incident.save()

    return jsonify({"message": "Incident saved successfully!", "incident_id": str(incident.id)}), 201


@incident_handlers.route('/<incident_id>', methods=['PUT'])
def update_incident(incident_id):
    data = request.json
    incident = crime.Incident.objects(id=incident_id).first()

    if not incident:
        return jsonify({"message": "Incident not found!"}), 404

    # Update fields if they are provided
    if 'description' in data:
        incident.description = data['description']
    if 'incident_type' in data:
        incident.incident_type = data['incident_type']
    if 'summary' in data:
        incident.summary = data['summary']
    if 'location' in data:
        incident.location = data['location']
    if 'occurred_at' in data:
        incident.occurred_at = data['occurred_at']

    incident.save()

    return jsonify({"message": "Incident updated successfully!"}), 200

@incident_handlers.route('/nearby', methods=['GET'])
def query_incidents():
    # Get the coordinates and radius from the query parameters
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('lon'))
    radius_km = float(request.args.get('radius', 10))  # Default to 10km if not provided

    distance_in_meters = radius_km * 1000

    # Query for nearby incidents
    nearby_incidents = crime.Incident.objects(
        location__near=[longitude, latitude],
        location__max_distance=distance_in_meters
    )

    # Convert the results to a list of dictionaries for JSON serialization
    incidents_list = [{"description": i.description, "location": i.location} for i in nearby_incidents]

    return jsonify(incidents_list)

