#!/usr/bin/python3

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response
from os import getenv
from flasgger import Swagger
from Flask_Cors import CORS, cross_origin

app = FLASK(__name__)
swagger = Swagger(app)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def close_db(error):
    """close storage"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """a handler for 404 errors that returns a JSON-formatted 404 status code response"""
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {\
        'title': 'AirBnB clone Restful API',
        'uiversion': 3
}

swagger

if __name__ == "__main__":
    app.run(host= os.getenv('HBNB_API_HOST'), port=os.getenv('HBNB_API_PORT'))
else:
    app.run(host='0.0.0.0', port='5000')
