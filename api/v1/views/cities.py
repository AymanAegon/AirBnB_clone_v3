#!/usr/bin/python3
"""States API routes"""
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_by_state(state_id):
    """Retrieves the list of all City objects of a State
    """
    arr = []
    all_cities = storage.all(City).values()
    for city in all_cities:
        if state_id == city.state_id:
            arr.append(city)
    if len(arr) != 0:
        return jsonify(arr)
    else:
        abort(404)


# @app_views.route('/states/', methods=['GET'], strict_slashes=False)
# def show_states():
#     """Shows all states in storage
#     """
#     states = list(storage.all(State).values())
#     states_array = []
#     for state in states:
#         states_array.append(state.to_dict())
#     return jsonify(states_array)


# @app_views.route(
#     '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
# def delete_state(state_id):
#     """Deletes a specific state based on id from storage
#     """
#     state = storage.get(State, state_id)
#     if state:
#         storage.delete(state)
#         storage.save()
#         return jsonify({})
#     else:
#         abort(404)


# @app_views.route('/states/', methods=['POST'], strict_slashes=False)
# def create_state():
#     """Creates a state object
#     """
#     content = request.get_json(silent=True)
#     error_message = ""
#     if type(content) is dict:
#         if "name" in content.keys():
#             state = State(**content)
#             storage.new(state)
#             storage.save()
#             response = jsonify(state.to_dict())
#             response.status_code = 201
#             return response
#         else:
#             error_message = "Missing name"
#     else:
#         error_message = "Not a JSON"

#     response = jsonify({'error': error_message})
#     response.status_code = 400
#     return response


# @app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
# def update_state(state_id):
#     """Updates an existing state object based on id
#     """
#     state = storage.get(State, state_id)
#     error_message = ""
#     if state:
#         content = request.get_json(silent=True)
#         if type(content) is dict:
#             ignore = ['id', 'created_at', 'updated_at']
#             for name, value in content.items():
#                 if name not in ignore:
#                     setattr(state, name, value)
#             storage.save()
#             return jsonify(state.to_dict())
#         else:
#             error_message = "Not a JSON"
#             response = jsonify({'error': error_message})
#             response.status_code = 400
#             return response
#     abort(404)
