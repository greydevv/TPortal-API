from flask import jsonify, make_response, Response
from typing import List, Any

class ApiException(Exception):
    def __init__(self, **kwargs):
        self.response = {}
        if hasattr(self, 'message'):
            self.response['message'] = self.message
        if kwargs:
            self.response = self.response | kwargs

    def get_response(self) -> Response:
        return make_response(self.response, self.code)

class DuplicateKeyError(ApiException):
    """
    Raised when an insertion POST request is made with an element that would
    create a duplicate key entry if it were to be entered into the database.
    """
    code = 409
    message = 'Could not add players to database as doing so would cause duplicate entries.'

class PlayerNotFoundError(ApiException):
    """
    Raised when a query for a player (by pid) is made, but the player does not 
    exist in the database.
    """
    code = 404
    message = 'Could not find the player with the specified pid.'
