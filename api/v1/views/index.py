#!/usr/bin/python3
"""
views
"""
from . import app_views
from flask import jsonify
from models import storage


classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}



# Define a route for /status
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """
    Return the status of your API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats',methods=['GET'], strict_slashes=False)
def api_stats():
    """
        return the number of objects
    """
    dict={}
    for key,value in classes.items():
        dict[key] = value.count()
    return jsonify({"status": "OK"})
