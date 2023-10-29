#!/usr/bin/python3
'''
app for registering blueprint and starting flask
'''
from flask import Flask
from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins="0.0.0.0")

# Register Blueprint
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


# Teardown app context to close the database connection
@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
