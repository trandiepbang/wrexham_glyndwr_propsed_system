from flask import jsonify

def not_found_error(error):
    return jsonify(error="Not Found"), 404

def internal_server_error(error):
    return jsonify(error="Internal Server Error"), 500
