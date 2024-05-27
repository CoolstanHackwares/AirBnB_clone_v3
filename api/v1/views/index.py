#!/usr/bin/python3
'''
    flask with general routes
    routes:
        /status:    display "status":"OK"
        /stats:     dispaly total for all classes
'''
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def storage_counts():
    '''
    Return counts of all classes in storage
    '''
    class_names = ["Amenity", "City", "Place", "Review", "State", "User"]
    cls_counts = {
        cls_name.lower() + "s": storage.count(cls_name)
        for cls_name in class_names
    }
    return jsonify(cls_counts)
