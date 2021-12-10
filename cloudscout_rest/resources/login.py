import datetime as dt
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from cloudscout_rest.ext import bcrypt, jwt, mongo
from cloudscout_rest.exceptions import UserNotRegisteredError, InvalidLoginError
from cloudscout_rest.schema import LOGIN
from cloudscout_rest.common.validate_json import assertjson

class Login(Resource):
    def post(self):
        users = mongo.db.users
        auth = request.authorization
        login_obj = users.find_one(
            {'login.email': auth['username']},
            {'login.email': True, 'login.password': True, '_id': False}
        )
        if not login_obj: 
            raise UserNotRegisteredError
            # return {'message': 'Email not registered'}

        login = login_obj['login']
        if not bcrypt.check_password_hash(login['password'], auth['password']):
            raise InvalidLoginError
        
        jwt_tok = create_access_token(identity=login['email'], expires_delta=dt.timedelta(minutes=60))
        return {'token': jwt_tok}, 200
