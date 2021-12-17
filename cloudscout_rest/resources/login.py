from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from cloudscout_rest.ext import bcrypt, jwt, mongo
from cloudscout_rest.exceptions import InvalidLoginError, NoAuthSuppliedError

class Login(Resource):
    def post(self):
        print(request.headers)
        # print("LOGGING USER IN: ", request.authorization)
        if not request.authorization:
            raise NoAuthSuppliedError
        users = mongo.db.users
        auth = request.authorization
        login_obj = users.find_one(
            {'login.email': auth['username']},
            {'login.email': True, 'login.password': True, '_id': False}
        )
        if not login_obj: 
            # user is not found in db
            raise InvalidLoginError

        login = login_obj['login']
        if not bcrypt.check_password_hash(login['password'], auth['password']):
            raise InvalidLoginError
        
        jwt_tok = create_access_token(identity=login['email'])
        ref_jwt_tok = create_refresh_token(identity=login['password'])
        return {'access_token': jwt_tok, 'refresh_token': ref_jwt_tok}, 200

class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        jwt_tok = create_access_token(identity=identity)
        return {'access_token': jwt_tok}

class Introspect(Resource):
    @jwt_required()
    def post(self):
        return '', 201
