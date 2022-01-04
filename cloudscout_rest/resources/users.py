from flask import request
from flask_restful import Resource
# from flask_jwt_extended import jwt_required
from cloudscout_rest.ext import bcrypt, mongo
from cloudscout_rest.exceptions import DuplicateKeyError, UserNotFoundError
from cloudscout_rest.schema import USER_POST
from cloudscout_rest.common.validate_json import assertjson

class Users(Resource):
    # @jwt_required()
    @assertjson(USER_POST)
    def post(self):
        users = mongo.db.users
        uid = request.json['uid']
        if users.find_one({'uid': uid}, {'_id': False}):
            raise DuplicateKeyError(data=uid)

        request.json['login']['password'] = bcrypt.generate_password_hash(request.json['login']['password']).decode('utf-8')
        users.insert_one(request.json)
        return uid, 200

class User(Resource):
    # @jwt_required()
    def get(self, uid):
        users = mongo.db.users
        data = users.find_one({'uid': uid}, {'_id': False})
        if not data:
            raise UserNotFoundError(data=uid)
        return data, 200

    # @jwt_required()
    def delete(self, uid):
        users = mongo.db.users
        result = users.delete_one({'uid': uid})
        if result.deleted_count == 0:
            raise UserNotFoundError(data=uid)
        return '', 204
