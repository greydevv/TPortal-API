from functools import wraps
import os
from flask import request, _request_ctx_stack
import requests
from jose import jwt
from cloudscout_rest.exceptions import AuthorizationError

def get_token_auth_header():
    '''
    Obtains the Access Token from the Authorization Header
    '''
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthorizationError(
            400,
            'Missing authorization header'
        )

    parts = auth.split()
    if parts[0].lower() != 'bearer' or len(parts) > 2:
        raise AuthorizationError(
            400, 
            "Header must be formatted as 'Bearer [token]'"
        )

    elif len(parts) == 1:
        raise AuthorizationError(
            400,
            'Token not found'
        )

    token = parts[1]
    print(token)
    return token

def auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
        AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')

        token = get_token_auth_header()
        jwks = requests.get(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json').json()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=['RS256'],
                    audience=AUTH0_AUDIENCE,
                    issuer=f'https://{AUTH0_DOMAIN}/'
                )
            except jwt.ExpiredSignatureError:
                raise AuthorizationError(
                    400, 
                    'Token expired'
                )
            except jwt.JWTClaimsError:
                raise AuthorizationError(
                    400,
                    'Invalid claims, please check the audience and issuer'
                )
            except Exception:
                raise AuthorizationError(
                    400,
                    'Unable to parse authentication token'
                )

            _request_ctx_stack.top.current_user = payload
            return func(*args, **kwargs)
        raise AuthorizationError(
            400,
            'Invalid header, unable to find appropriate key'
        )
    return decorated
