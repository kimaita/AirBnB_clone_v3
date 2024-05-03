#!/usr/bin/python3
"""Handles REST requests for Amenities"""

from api.v1.app import storage
from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, request, abort


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    """Returns a list of all amenities"""
    amenities = storage.all(Amenity)

    return jsonify([obj.to_dict() for obj in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Returns a single Amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return amenity.to_dict()


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity from POST data and persists it in storage
    """
    amenity_dict = request.get_json()
    if not amenity_dict:
        abort(400, 'Not a JSON')
    if 'name' not in amenity_dict:
        abort(400, 'Missing name')

    amenity = Amenity(**amenity_dict)
    amenity.save()
    return amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates Amenity properties"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity_dict = request.get_json()
    if not amenity_dict:
        abort(400, 'Not a JSON')

    ignore = ['id', 'created_at', 'updated_at']

    for attr, val in amenity_dict.items():
        if attr not in ignore:
            setattr(amenity, attr, val)
    amenity.save()

    return amenity.to_dict(), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity, returning an empty dict"""

    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()
    return {}, 200
