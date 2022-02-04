from flask import request
from flask_restful import Resource
from cloudscout_rest.ext import bcrypt, mongo
from cloudscout_rest.exceptions import DuplicateKeyError, ResourceNotFoundError
from cloudscout_rest.schemas.schema import USER
from cloudscout_rest.common.auth_required import auth_required
from cloudscout_rest.common.validate_json import assertuser

class Users(Resource):
    @auth_required
    @assertuser
    def post(self):
        users = mongo.db.users
        uid = request.json['uid']
        if users.find_one({'uid': uid}, {'_id': False}):
            raise DuplicateKeyError(data=uid)
        users.insert_one(request.json)
        return {}, 200

class User(Resource):
    @auth_required
    def get(self, uid):
        users = mongo.db.users
        data = users.find_one({'uid': uid}, {'_id': False})
        if not data:
            raise ResourceNotFoundError(data=uid)
        return data, 200

    @auth_required
    @assertuser
    def put(self, uid):
        users = mongo.db.users
        if not users.find_one({'uid': uid}):
            raise ResourceNotFoundError(data=uid)

        # check if user is attempting to update uid and check if it would cause
        # a duplicate
        if request.json['uid'] != uid and users.find_one({'uid': request.json['uid']}) is not None:
            raise DuplicateKeyError(data=uid)
        result = users.replace_one({'uid': uid}, request.json)
        return {}, 200

    @auth_required
    def delete(self, uid):
        users = mongo.db.users
        result = users.delete_one({'uid': uid})
        if result.deleted_count == 0:
            raise ResourceNotFoundError(data=uid)
        return {}, 200
