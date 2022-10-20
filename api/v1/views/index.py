#!/usr/bin/python3
"""route /status on the obj app_views that returns json string status ok"""
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """api status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def object_number():
    """retrieves number of each object by type"""
    classes = [Amenity, City, Place, Review, State, User]
    att = ["amenities", "cities", "places", "reviews", "states", "users"]

    obj_num = {}
    for i in range(len(classes)):
        obj_num[att[i]] = storage.count(classes[i])

    return jsonify(obj_num)
