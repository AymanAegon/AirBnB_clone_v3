#!/usr/bin/python3
"""places_amenities API routes"""
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort
from os import getenv
storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route(
    '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def amenity_by_place(place_id):
    """Retrieves the list of all Amenity objects of a Place
    """
    if storage_t == "db":
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        print(place)
    else:
        pass
