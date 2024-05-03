#!/usr/bin/python3
"""Instantiates the app_views Blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
states = Blueprint('states', __name__, url_prefix='/states')
app_views.register_blueprint(states)

from api.v1.views.index import *
from api.v1.views.states import *
