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
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    arr = []
    for amenity in place.amenities:
        arr.append(amenity.to_dict())
    return jsonify(arr)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['POST'], strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """Link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        abort(404)
    place.amenities.append(amenity)
    storage.save()
    response = jsonify(amenity.to_dict())
    response.status_code = 201
    return response
