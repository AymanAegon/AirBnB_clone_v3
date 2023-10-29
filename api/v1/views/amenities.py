#!/usr/bin/python3
"""States API routes"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all amenities
    """
    all = storage.all(Amenity).values()
    arr = []
    for amenity in all:
        arr.append(amenity.to_dict())
    return jsonify(arr)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def show_amenity(amenity_id):
    """Retrieves a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a specific amenity based on id from storage
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a amenity object
    """
    content = request.get_json(silent=True)
    error_message = ""
    if type(content) is dict:
        if "name" in content.keys():
            amenity = Amenity(**content)
            storage.new(amenity)
            storage.save()
            response = jsonify(amenity.to_dict())
            response.status_code = 201
            return response
        else:
            error_message = "Missing name"
    else:
        error_message = "Not a JSON"

    response = jsonify({'error': error_message})
    response.status_code = 400
    return response


@app_views.route(
    '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an existing state object based on id
    """
    amenity = storage.get(Amenity, amenity_id)
    error_message = ""
    if amenity:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'created_at', 'updated_at']
            for name, value in content.items():
                if name not in ignore:
                    setattr(amenity, name, value)
            storage.save()
            return jsonify(amenity.to_dict())
        else:
            error_message = "Not a JSON"
            response = jsonify({'error': error_message})
            response.status_code = 400
            return response
    abort(404)
