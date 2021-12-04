import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
from tportal_rest.ext import mongo
from tportal_rest.resources.players import Players, Player
from tportal_rest.exceptions import ApiException

class TPortalREST(Api):
    def handle_error(self, e):
        if isinstance(e, ApiException):
            return e.get_response()
        return super().handle_error(e)

def get_mongo_uri():
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
        raise ValueError('No MONGO_URI specified.')
    return MONGO_URI

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['MONGO_URI'] = get_mongo_uri()

    mongo.init_app(app)

    api = TPortalREST(app)
    api.add_resource(Players, '/v1/players')
    api.add_resource(Player, '/v1/players/<string:pid>')
    return app
