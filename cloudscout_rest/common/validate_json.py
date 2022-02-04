from flask import request
from functools import wraps
from cloudscout_rest.schemas.base import PlayerSchema
from cloudscout_rest.schemas.players import SPORT_NAME_MAPPING 
from cloudscout_rest.schemas.schema import USER
from jsonschema import ValidationError, validate

class NoJsonError(Exception):
    message = 'No JSON supplied'

def assertplayer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try: 
            # initial validation to get sport
            validate(request.json, PlayerSchema.get_skeleton())
            sport = request.json['meta']['sport']
            validate(request.json, {
                'type': 'array',
                'items': SPORT_NAME_MAPPING[sport].raw()
            })
        except ValidationError as err:
            return responsify_err(err)
        return func(*args, **kwargs)
    return inner

def assertuser(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            validate(request.json, USER)
        except ValidationError as err:
            return responsify_err(err)
        return func(*args, **kwargs)
    return inner

def responsify_err(err):
    payload = {
        'msg': 'Invalid JSON',
        'json': request.json,
        'reason': err.message
    } 
    return payload, 400
