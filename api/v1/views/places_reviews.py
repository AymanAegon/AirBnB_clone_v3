#!/usr/bin/python3
"""States API routes"""
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    arr = []
    for review in place.reviews:
        arr.append(review.to_dict())
    return jsonify(arr)


@app_views.route(
    '/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_one_review(review_id):
    """Retrieves a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """deletes a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        return abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route(
    '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """create a Review object
    """
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    content = request.get_json(silent=True)
    if type(content) is not dict:
        response = jsonify({'error': "Not a JSON"})
        response.status_code = 400
        return response
    if "user_id" not in content.keys():
        response = jsonify({'error': "Missing user_id"})
        response.status_code = 400
        return response
    user = storage.get(User, content["user_id"])
    if not user:
        abort(404)
    if "text" not in content.keys():
        response = jsonify({'error': "Missing text"})
        response.status_code = 400
        return response
    review = Review(**content)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    response = jsonify(review.to_dict())
    response.status_code = 201
    return response


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    content = request.get_json(silent=True)
    if type(content) is not dict:
        response = jsonify({'error': "Not a JSON"})
        response.status_code = 400
        return response
    for key, value in content:
        ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())
