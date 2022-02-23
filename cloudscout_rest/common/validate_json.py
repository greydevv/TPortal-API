from flask import request
from functools import wraps
from cloudscout_rest.schemas.base import PlayerSchema
from cloudscout_rest.schemas.players import SPORT_NAME_MAPPING 
from cloudscout_rest.schemas.schema import USER, IDS
from cloudscout_rest.exceptions import InvalidJsonError
from jsonschema import ValidationError, validate

def assertplayer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try: 
            # initial JSON validation steps
            if not isinstance(request.json, list):
                raise InvalidJsonError(msg=f"Invalid JSON: {request.json} is not of type 'array'")
            if len(request.json) == 0:
                raise InvalidJsonError(msg='Invalid JSON: Cannot supply an empty array')
            # expects array of players, so validate each one for custom error
            # messages on different sports
            for player in request.json:
                validate(player, PlayerSchema.get_skeleton())
                sport = player['meta']['sport']
                # validating players differently based on their sports as each
                # sport has different schemas
                validate(player, SPORT_NAME_MAPPING[sport].raw())
        except ValidationError as err:
            raise InvalidJsonError(msg=f'Invalid JSON: {err.message}')
        return func(*args, **kwargs)
    return inner

def _basic_validate(schema):
    try:
        validate(request.json, schema)
    except ValidationError as err:
        raise InvalidJsonError(msg=f'Invalid JSON: {err.message}')

def assertuser(func):
    @wraps(func)
    def inner(*args, **kwargs):
        _basic_validate(USER)
        return func(*args, **kwargs)
    return inner

def assertids(func):
    @wraps(func)
    def inner(*args, **kwargs):
        _basic_validate(IDS)
        return func(*args, **kwargs)
    return inner
