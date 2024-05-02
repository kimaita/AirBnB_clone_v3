#!/usr/bin/python3
""" Defines routes on the API """
from api.v1.views import app_views
from api.v1.app import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns a status OK message"""
    return {'status': 'OK'}


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_object_stats():
    """Retrieves object counts by type"""
    classes = {'amenities': Amenity, 'cities': City, 'places': Place,
               'reviews': Review, 'states': State, 'users': User}

    objs = {k: storage.count(v) for k, v in classes.items()}
    return objs
