#!/usr/bin/python3
"""Handles REST requests for State objects"""

from api.v1.app import storage
from api.v1.views import app_views
from models.state import State
from flask import jsonify, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Returns a list of all States"""
    objs = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(objs)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object from POST data and persists it in storage
    """
    state_dict = request.get_json()

    if not state_dict:
        abort(400, 'Not a JSON')

    if 'name' not in state_dict:
        return 'Missing Name', 400

    state = State(**state_dict)
    state.save()
    return state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Returns a single State objct, by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return state.to_dict()


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates State object properties"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state_dict = request.get_json()
    if not state_dict:
        abort(400, 'Not a JSON')

    ignore = ['id', 'created_at', 'updated_at']

    for attr, val in state_dict.items():
        if attr not in ignore:
            setattr(state, attr, val)
    state.save()

    return state.to_dict(), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object, returning an empty dict"""

    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()
    return {}, 200
