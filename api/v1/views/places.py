#!/usr/bin/python3
"""Places API routes"""
from models import storage
from flask import jsonify, request
from api.v1.views import app_views
from api.v1.app import not_found
from models.place import Place
from models.city import City


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def show_places(city_id):
    """
           A list of JSON dictionaries of all places in a city
    """
    city = storage.get(City, city_id)
    places_list = []
    if city:
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        return not_found(404)



@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes place
    """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        return not_found(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id):
    """Shows places
    """
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return not_found(404)



@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a place
    """
    place = storage.get('Place', place_id)
    if place:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for name, value in content.items():
                if name not in ignore:
                    setattr(place, name, value)
            storage.save()
            return jsonify(place.to_dict())

        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        return not_found(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''
        create new place
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    else:
        obj_data = request.get_json()
        city = storage.get("City", city_id)
        user = storage.get("User", obj_data['user_id'])
        if city is None or user is None:
            abort(404)
        obj_data['city_id'] = city.id
        obj_data['user_id'] = user.id
        obj = Place(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201
