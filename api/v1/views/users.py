#!/usr/bin/python3
"""Handles REST requests for User objects"""

from api.v1.app import storage
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Returns a list of all users"""
    users = storage.all(User)

    return jsonify([obj.to_dict() for obj in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Returns a single User by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return user.to_dict()


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User from POST data and persists it in storage
    """
    user_dict = request.get_json()
    if not user_dict:
        abort(400, 'Not a JSON')
    if 'email' not in user_dict:
        abort(400, 'Missing email')
    if 'password' not in user_dict:
        abort(400, 'Missing password')

    user = User(**user_dict)
    user.save()
    return user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates User properties"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user_dict = request.get_json()
    if not user_dict:
        abort(400, 'Not a JSON')

    ignore = ['id', 'email', 'created_at', 'updated_at']

    for attr, val in user_dict.items():
        if attr not in ignore:
            setattr(user, attr, val)
    user.save()

    return user.to_dict(), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user, returning an empty dict"""

    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()
    return {}, 200
