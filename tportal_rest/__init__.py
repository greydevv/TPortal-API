from flask import Flask
from dotenv import load_dotenv
import os

def get_mongo_uri():
    load_dotenv()
    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
        raise ValueError('No MONGO_URI specified.')
    return MONGO_URI

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = get_mongo_uri()

    return app
