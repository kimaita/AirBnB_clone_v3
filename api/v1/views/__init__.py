#!/usr/bin/python3
"""Instantiates flask Blueprints"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
states = Blueprint('states', __name__, url_prefix='/states')
cities = Blueprint('cities', __name__, url_prefix='/cities')

app_views.register_blueprint(states)
app_views.register_blueprint(cities)

from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.states import *
