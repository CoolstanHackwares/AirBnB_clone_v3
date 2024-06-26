#!/usr/bin/python3
'''
    RESTful API for State class
'''
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''
    Retrieve list of all State objects
    '''
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''
    Retrieve a State object by id
    '''
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''
    Delete a State object by id
    '''
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''
    Create a new State object
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''
    Update a State object by id
    '''
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
