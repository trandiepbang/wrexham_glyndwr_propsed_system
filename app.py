from flask import Flask
from libs import mongodb
from handlers import error_handlers, incidents_handlers
from handlers import teardown_handlers
from handlers import users_handlers
from handlers import location_handlers


app = Flask(__name__)


if __name__ == "__main__":
    app.register_blueprint(users_handlers.users_handlers, url_prefix='/v1/users')
    app.register_blueprint(location_handlers.location_handlers, url_prefix='/v1/location')
    app.register_blueprint(incidents_handlers.incident_handlers, url_prefix='/v1/admin/incident')

    # Register error handlers
    app.register_error_handler(404, error_handlers.not_found_error)
    app.register_error_handler(500, error_handlers.internal_server_error)

    # Register teardown handler
    app.teardown_appcontext(teardown_handlers.teardown_appcontext)

    app.run(host='0.0.0.0', port='8080', debug=True)