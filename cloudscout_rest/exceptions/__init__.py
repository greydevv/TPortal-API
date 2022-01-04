from flask import jsonify, make_response, Response
from typing import List, Any

class ApiException(Exception):
    def __init__(self, **kwargs):
        self.response = {}
        if hasattr(self, 'message'):
            self.response['msg'] = self.message
        elif hasattr(self, 'msg'):
            self.response['msg'] = self.msg
        if kwargs:
            self.response = self.response | kwargs

    def get_response(self) -> Response:
        return make_response(self.response, self.code)


# AUTHORIZATION

class AuthorizationError(ApiException):
    """
    Raised when authorization fails for a protected resource.
    """
    def __init__(self, code=401, msg='Unauthorized', **kwargs):
        super().__init__(code=code, msg=msg, **kwargs)
        self.code = code
        self.msg = msg

# PLAYERS

class DuplicateKeyError(ApiException):
    """
    Raised when an insertion POST request is made with an element that would
    create a duplicate key entry if it were to be entered into the database.
    """
    code = 409
    msg = 'Could not add players to database as doing so would cause duplicate entries'

class PlayerNotFoundError(ApiException):
    """
    Raised when a query for a player (by pid) is made, but the player does not 
    exist in the database.
    """
    code = 404
    msg = 'Could not find the player with the specified pid'


# USERS

class UserNotFoundError(ApiException):
    """
    Raised when a query for a user (by uid) is made, but the uid does not 
    exist in the database.
    """
    code = 404
    msg = 'Could not find the user with the specified pid'


# LOGIN

class InvalidLoginError(ApiException):
    """
    Raised when a user attmepts to login with invalid credentials.
    """
    code = 401
    msg = 'Incorrect username or password'

class NoAuthSuppliedError(ApiException):
    """
    Raised when a user attempts to login with no credentials.
    """
    code = 400
    msg = 'Missing authorization header'
