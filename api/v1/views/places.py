#!/usr/bin/python3
"""Handles REST requests for City objects"""

from api.v1.app import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, request, abort


@app_views.route('cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """Returns a list of all places in a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    objs = [obj.to_dict() for obj in city.places]
    return jsonify(objs)


@app_views.route('places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Returns a single Place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return place.to_dict()


@app_views.route('cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new Place from POST data and persists it in storage
    """
    place_dict = request.get_json()
    if not place_dict:
        abort(400, 'Not a JSON')

    if 'name' not in place_dict:
        abort(400, 'Missing name')

    if 'user_id' not in place_dict:
        abort(400, 'Missing user_id')
    user = storage.get(User, place_dict.get('user_id'))
    if not user:
        abort(404)

    place = Place(**place_dict)
    place.city_id = city_id
    place.save()
    return place.to_dict(), 201


@app_views.route('places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a place's properties"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place_dict = request.get_json()
    if not place_dict:
        abort(400, 'Not a JSON')

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for attr, val in place_dict.items():
        if attr not in ignore:
            setattr(place, attr, val)
    place.save()

    return place.to_dict(), 200


@app_views.route('places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a place, returning an empty dict"""

    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()
    return {}, 200
