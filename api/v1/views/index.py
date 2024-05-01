#!/usr/bin/python3
"""defines routes for the API"""
from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    """Returns a status OK message"""
    return {'status': 'OK'}
