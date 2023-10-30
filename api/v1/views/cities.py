#!/usr/bin/python3
"""States API routes"""
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_by_state(state_id):
    """Retrieves the list of all City objects of a State
    """
    arr = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = storage.all(City).values()
    for city in all_cities:
        if state_id == city.state_id:
            arr.append(city.to_dict())
    return jsonify(arr)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def show_city(city_id):
    """Shows a specific city based on id from storage
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a specific city based on id from storage
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a city object
        Returns: the new city
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    content = request.get_json(silent=True)
    error_message = ""
    if type(content) is dict:
        if "name" in content.keys():
            city = City(**content)
            city.state_id = state_id
            storage.new(city)
            storage.save()
            response = jsonify(city.to_dict())
            response.status_code = 201
            return response
        else:
            error_message = "Missing name"
    else:
        error_message = "Not a JSON"

    response = jsonify({'error': error_message})
    response.status_code = 400
    return response


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates an existing city object based on id
    """
    city = storage.get(City, city_id)
    error_message = ""
    if city:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'state_id', 'created_at', 'updated_at']
            for name, value in content.items():
                if name not in ignore:
                    setattr(city, name, value)
            storage.save()
            return jsonify(city.to_dict())
        else:
            error_message = "Not a JSON"
            response = jsonify({'error': error_message})
            response.status_code = 400
            return response
    abort(404)
