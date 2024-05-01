#!/usr/bin/python3
"""Runs a Flask web server"""

from api.v1.views import app_views
from models import storage
from flask import Flask
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    storage.close()


if __name__ == "__main__":

    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host, port, threaded=True)