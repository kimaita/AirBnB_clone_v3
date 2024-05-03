#!/usr/bin/python3
"""Handles REST requests for City objects"""

from api.v1.app import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from flask import jsonify, request, abort


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Returns a single City by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return city.to_dict()


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_state_cities(state_id):
    """Returns a list of all cities for the State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    objs = [obj.to_dict() for obj in state.cities]
    return jsonify(objs)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new City from POST data and persists it in storage
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_dict = request.get_json()
    if not city_dict:
        abort(400, 'Not a JSON')
    if 'name' not in city_dict:
        abort(400, 'Missing name')

    city = City(**city_dict)
    city.state_id = state.id
    city.save()
    return city.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates City object properties"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city_dict = request.get_json()
    if not city_dict:
        abort(400, 'Not a JSON')

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    for attr, val in city_dict.items():
        if attr not in ignore:
            setattr(city, attr, val)
    city.save()

    return city.to_dict(), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object, returning an empty dict"""

    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()
    return {}, 200
