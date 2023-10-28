!/usr/bin/python3
"""States API routes"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort




@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def show_state(state_id):
    """Shows a specific state based on id from storage
           Parameters:
    """
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def show_states():
    """Shows all states in storage
    """
    states = list(storage.all('State').values())
    states_array = []
    for state in states:
        states_array.append(state.to_dict())
    return jsonify(states_array)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a specific state based on id from storage
    """
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)
