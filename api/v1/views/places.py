#!/usr/bin/python3
"""Places API routes"""
from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.state import State



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
        return abort(404)



@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes place
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        return abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id):
    """Shows places
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)



@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a place
    """
    place = storage.get(Place, place_id)
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
        return abort(404)


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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    '''
        Searches for places
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    arr = []
    result = []
    states = []
    cities = []
    amenities = []
    if "states" in request.get_json():
        states = request.get_json()["states"]
    if "cities" in request.get_json():
        cities = request.get_json()["cities"]
    if "amenities" in request.get_json():
        amenities = request.get_json()["amenities"]
    all_places = storage.all(Place).values()
    for place in all_places:
        city_of_place = storage.get(City, place.city_id)
        if states is None or len(states) == 0:
            if place not in result:
                result.append(place)
        elif city_of_place.state_id in states:
            if place not in result:
                result.append(place)
        if cities is None or len(cities) == 0:
            if place not in result:
                result.append(place)
        elif place.city_id in cities:
            if place not in result:
                result.append(place)

    if amenities is None or len(amenities) == 0:
        for place in result:
            arr.append(place.to_dict())
        return jsonify(arr)

    for place in result:
        for amenity_id in amenities:
            if amenity_id not in place.amenities:
                result.remove(place)
                break

    for place in result:
        arr.append(place.to_dict())
    return jsonify(arr)
