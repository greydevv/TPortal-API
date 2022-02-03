from flask import request
from functools import wraps
from jsonschema import ValidationError, validate

class NoJsonError(Exception):
    message = 'No JSON supplied'

def assertjson(schema):
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if not request.json:
                return responsify_err(NoJsonError)
            try:
                if isinstance(schema, list):
                    # for accepting multiple schemas
                    errors = None
                    for s in schema:
                        try: 
                            validate(request.json, s)
                            return func(*args, **kwargs)
                        except ValidationError as err:
                            errors = err
                    if errors:
                        return responsify_err(errors)
                else:
                    validate(request.json, schema)
            except ValidationError as err:
                return responsify_err(err)
            return func(*args, **kwargs)
        return decorated
    return wrapper

def responsify_err(err):
    payload = {
        'message': 'Invalid JSON',
        'json': request.json,
        'reason': err.message
    } 
    return payload, 400
