import os
from datetime import timedelta
from flask import Flask
from flask.json import JSONEncoder
from flask_restful import Api
from flask_cors import CORS
from bson import ObjectId
from werkzeug.routing import BaseConverter
from dotenv import load_dotenv
from cloudscout_rest.ext import mongo
from cloudscout_rest.resources.players import Players, Player
from cloudscout_rest.resources.users import Users, User
from cloudscout_rest.resources.analysis import Analysis
from cloudscout_rest.exceptions import ApiException

class CloudscoutApi(Api):
    """
    A subclass of the flask_restful 'Api' object for custom behavior.
    """
    def handle_error(self, e):
        # handle custom errors
        if isinstance(e, ApiException):
            return e.get_response()
        return super().handle_error(e)

def get_env_or_raise(key):
    value = os.getenv(key)
    if not value:
        raise ValueError(f'No {key} specified.')
    return value

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    # raise ValueError if required environment variables are not present
    app.config['MONGO_URI'] = get_env_or_raise('MONGO_URI')
    get_env_or_raise('AUTH0_DOMAIN')
    get_env_or_raise('AUTH0_AUDIENCE')
    
    mongo.init_app(app)

    api = CloudscoutApi(app)
    api.add_resource(Players, '/v1/players')
    api.add_resource(Player, '/v1/players/<string:pid>')

    api.add_resource(Users, '/v1/users')
    api.add_resource(User, '/v1/users/<string:uid>')

    api.add_resource(Analysis, '/v1/analysis')
    return app
