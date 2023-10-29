#!/usr/bin/python3
"""States API routes"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves the list of all users
    """
    users = storage.all(User).values()
    arr = []
    for user in users:
        arr.append(user.to_dict())
    return jsonify(arr)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def show_users(user_id):
    """Retrieves a User object
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route(
    '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a specific user based on id from storage
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a user object
    """
    content = request.get_json(silent=True)
    error_message = ""
    if type(content) is dict:
        if "email" not in content.keys():
            error_message = "Missing email"
        elif "password" not in content.keys():
            error_message = "Missing password"
        else:
            user = User(**content)
            storage.new(user)
            storage.save()
            response = jsonify(user.to_dict())
            response.status_code = 201
            return response
    else:
        error_message = "Not a JSON"

    response = jsonify({'error': error_message})
    response.status_code = 400
    return response


@app_views.route(
    '/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates an existing user object based on id
    """
    user = storage.get(User, user_id)
    error_message = ""
    if user:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'email', 'created_at', 'updated_at']
            for name, value in content.items():
                if name not in ignore:
                    setattr(user, name, value)
            storage.save()
            return jsonify(user.to_dict())
        else:
            error_message = "Not a JSON"
            response = jsonify({'error': error_message})
            response.status_code = 400
            return response
    abort(404)
