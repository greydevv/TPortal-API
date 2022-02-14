from flask import request
from functools import wraps
from cloudscout_rest.schemas.base import PlayerSchema
from cloudscout_rest.schemas.players import SPORT_NAME_MAPPING 
from cloudscout_rest.schemas.schema import USER
from cloudscout_rest.exceptions import InvalidJsonError
from jsonschema import ValidationError, validate

class NoJsonError(Exception):
    message = 'No JSON supplied'

def assertplayer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try: 
            # initial validation to get sport
            for player in request.json:
                validate(player, PlayerSchema.get_skeleton())
                sport = player['meta']['sport']
                validate(player, SPORT_NAME_MAPPING[sport].raw())
        except ValidationError as err:
            raise InvalidJsonError(msg=f'Invalid JSON: {err.message}')
        return func(*args, **kwargs)
    return inner

def assertuser(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            validate(request.json, USER)
        except ValidationError as err:
            raise InvalidJsonError(msg=f'Invalid JSON: {err.message}')
        return func(*args, **kwargs)
    return inner
