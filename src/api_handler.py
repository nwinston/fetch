import datetime
from typing import Dict
from .database.in_memory_database import InMemoryDatabase
from .util.decorators import handle_api_response
from .timestamp_exception import TimestampException

class APIHandler:
    """
    An abstraction layer for handling API calls. This class is responsible for
    interacting with the database and returning the appropriate response.
    """
    def __init__(self):
        self.database = InMemoryDatabase()

    @handle_api_response
    def create_user(self, user) -> None:
        """
        Creates and regisiters a user to the database.

        Args:
            user (str): The user to create.
        """
        self.database.create_user(user)

    @handle_api_response
    def spend_points(self, user, points) -> Dict[str, int]:
        """
        Spends points from the user's account.

        Args:
            user (str): The user spending points.
            points (int):  The number of points to spend.

        Returns:
            Dict[str, int]: A dictionary mapping payers to the number of points they provided for this user's spending.
        """
        return self.database.spend_points(user, points)

    @handle_api_response
    def get_points(self, user) -> Dict[str, int]:
        """
        Gets the point balances for each payer for the given user.

        Args:
            user (str): The user to get the point balances for.

        Returns:
            Dict[str, int]: Point balances for each payer for the given user.
        """
        return self.database.get_points(user)

    @handle_api_response
    def get_total_points(self, user) -> int:
        """
        Returns the total points for the given user.

        Args:
            user (str): The user

        Returns:
            int: Total points for the given user
        """
        return self.database.get_total_points(user)

    @handle_api_response
    def create_transaction(self, user: str, payer: str, points: int, timestamp: str) -> None:
        """
        Adds a transaction to the database.

        Args:
            user (str): The user
            payer (str): The payer who is providing the points.
            points (int): The number of points being provided.
            timestamp (str): The timestamp of the transaction.

        Raises:
            TimestampException: If the timestamp is not in the correct format.
        """
        try:
            iso_timestamp = timestamp.replace("Z", "+00:00")
            timestamp_dt = datetime.datetime.fromisoformat(iso_timestamp)
        except ValueError as e:
            raise TimestampException(f"Invalid timestamp: {timestamp}. Timestamp must be in form of YYYY-MM-DDTHH:MM:SSZ")

        self.database.add_transaction(user, payer, points, timestamp_dt)