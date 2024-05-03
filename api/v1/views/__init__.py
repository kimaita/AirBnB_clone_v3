#!/usr/bin/python3
"""Instantiates flask Blueprints"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places import *
from api.v1.views.states import *
from api.v1.views.users import *

app_views.register_blueprint(states)
app_views.register_blueprint(cities)
app_views.register_blueprint(amenities)
app_views.register_blueprint(users)
app_views.register_blueprint(places)
