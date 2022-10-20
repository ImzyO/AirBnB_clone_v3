#!/usr/bin/python3

from api.v1.views import app_views
from models import storage
from flask import Flask
from os import getenv

app = FLASK(__name__)

@app.teardown_appcontext
def close_db():
    """close storage"""
    storage.close()

if __name__ == "__main__":
    app.run(host= os.getenv('HBNB_API_HOST'), port=os.getenv('HBNB_API_PORT'))
else:
    app.run(host='0.0.0.0', port='5000')
