import os
from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from cloudscout_rest.ext import mongo
from cloudscout_rest.resources.players import Players, Player
from cloudscout_rest.resources.users import Users, User
from cloudscout_rest.exceptions import ApiException

class TPortalREST(Api):
    """
    A subclass of the flask_restful 'Api' object for custom behavior.
    """
    def handle_error(self, e):
        if isinstance(e, ApiException):
            return e.get_response()
        return super().handle_error(e)

def get_or_raise(key):
    value = os.getenv(key)
    if not value:
        raise ValueError(f'No {key} specified.')
    return value

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    app.config['MONGO_URI'] = get_or_raise('MONGO_URI')
    get_or_raise('AUTH0_DOMAIN')
    get_or_raise('AUTH0_AUDIENCE')
    mongo.init_app(app)

    api = TPortalREST(app)
    api.add_resource(Players, '/v1/players')
    api.add_resource(Player, '/v1/players/<string:pid>')

    api.add_resource(Users, '/v1/users')
    api.add_resource(User, '/v1/users/<string:pid>')
    return app
