from . import app_views
from flask import jsonify

# Define a route for /status
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """
    Return the status of your API
    """
    return jsonify({"status": "OK"})

