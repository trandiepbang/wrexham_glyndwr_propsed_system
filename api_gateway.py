import requests
from flask import Flask
from flask import request, jsonify
from libs import jwt

app = Flask(__name__)


protected_path = [
    "/v1/location/update",
]

protected_full_endpoint = [
    "/v1/admin/incident"
]

@app.route("/v1/<path:subpath>", methods=['POST','GET'])
def api_gateway_authentication(subpath):
    token = None
    current_user_id = None

    try:
        if request.path in protected_path:
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].replace("Bearer ", "")
                
            if not token:
                return jsonify({"message": "Token is missing!"}), 401
                
            # Decode the token cause its protected path
            payload = jwt.decode(token)
            current_user_id = payload['user_id']

        # Get the original path and method from the incoming request
        original_path = request.path
        original_method = request.method.lower()  # this will be 'get', 'post', etc.

        
        # Construct the URL for the internal service
        internal_service_url = f"http://localhost:8080{original_path.replace('/1', '')}"

        headers = {
            "Content-Type": "application/json",
        }

        if current_user_id is not None:
            headers['Authorization'] = f"Bearer {token}"
            headers['Current-User-ID'] = current_user_id

        # Use the original HTTP method to forward the request
        response = getattr(requests, original_method)(internal_service_url, headers=headers, json=request.json)

        if response.status_code == 200:
            return response.json(), 200
        else:
            return response.json(), response.status_code

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='9000', debug=True)