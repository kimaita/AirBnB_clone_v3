#!/usr/bin/python3
"""Instantiates flask Blueprints"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
states = Blueprint('states', __name__, url_prefix='/states')
cities = Blueprint('cities', __name__, url_prefix='/cities')
amenities = Blueprint('amenities', __name__, url_prefix='/amenities')
users = Blueprint('users', __name__, url_prefix='/users')

app_views.register_blueprint(states)
app_views.register_blueprint(cities)
app_views.register_blueprint(amenities)
app_views.register_blueprint(users)

from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.users import *
