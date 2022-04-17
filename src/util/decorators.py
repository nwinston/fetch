import functools

from flask import Response, make_response, jsonify

from ..timestamp_exception import TimestampException
from ..database.database_exception import DatabaseException

def db_error_handler(func):
    """
    Decorator for handling database errors.

    Raises:
        e: Any unhadled exception.
        DatabaseException: An exception from the database.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise DatabaseException(f"An unexpected error occurred: {e}")
    return inner

def handle_api_response(func) -> 'function':
    """
    Decorator for handling API responses.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs) -> Response:
        """
        Handles any errors from the api call and returns a flask response.

        Returns:
            Response: A flask response.
        """
        try:
            result = func(*args, **kwargs)
            if not isinstance(result, int) and not result:
                result = {}
            response = make_response(jsonify(response=result, success=True), 200)
        except DatabaseException as e:
            response = make_response(jsonify(response=e.message, success=False), 500)
        except TimestampException as e:
            response = make_response(jsonify(response=e.message, success=False), 400)

        return response
    return inner