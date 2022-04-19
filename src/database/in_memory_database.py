from collections import defaultdict
import datetime

import heapq
from typing import Dict

from ..util.decorators import db_error_handler
from . import database
from .database_exception import DatabaseException

class Transaction:
    """
    Data class for a transaction. Implements the __lt__ method for use in the heapq
    to be sorted by transaction timestamp.
    """
    def __init__(self, payer, points, timestamp):
        self._payer = payer
        self._points = points
        self._timestamp = timestamp

    def __lt__(self, other: 'Transaction'):
        return self.timestamp < other.timestamp

    @property
    def payer(self):
        return self._payer
    
    @property
    def points(self):
        return self._points

    @property
    def timestamp(self):
        return self._timestamp


class InMemoryDatabase(database.Database):
    """
    
    This class is responsible for maintaining a database of user point balances and transactions
    so that the user's points are spent in the correct order based on transaction timestamp. To 
    achieve this, the transactions are stored in a min heap using the timestamp as the key.

    """

    def __init__(self):
        self.transactions = {}
        self.point_totals = {}
        self.users = set()

    @db_error_handler
    def add_transaction(self, user: str, payer: str, points: int, timestamp: datetime.datetime) -> None:
        """
        Adds a transaction to the database.

        Args:
            user (str): The user
            payer (str): The payer who is providing the points.
            points (int): The number of points being provided.
            timestamp (datetime.datetime): The timestamp of the transaction.

        Raises:
            DatabaseException: If the user does not exist.
        """
        self.check_user_exists(user)

        self.point_totals[user][payer] += points
        transaction = Transaction(payer, points, timestamp)
        heapq.heappush(self.transactions[user], transaction)


    @db_error_handler
    def create_user(self, user: str) -> None:
        """
        Creates and regisiters a user to the database.

        Args:
            user (str): The user to create.

        Raises:
            DatabaseException: If the user already exists.
        """
        if user not in self.users:
            self.users.add(user)
            self.transactions[user] = []
            self.point_totals[user] = defaultdict(int)
        else:
            raise DatabaseException(f'{user} already exists')

    @db_error_handler
    def spend_points(self, user: str, points: int) -> Dict[str, int]:
        """
        Spends the given number of points from the user's account. Raises
        an exception if the user does not have enough points.

        Args:
            user (str): The user spending the points.
            points (int): The number of points being spent.

        Returns:
            Dict[str, int]: A dictionary mapping payers to the number of points they provided for this user's spending.

        Raises:
            DatabaseException: If the user does not have enough points or the user does not exist.
        """
        self.check_user_exists(user)
        if points > self.get_total_points(user):
            raise DatabaseException(f'user {user} does not have enough points to spend')

        spent_points = defaultdict(int)
        while points > 0:
            transaction = heapq.heappop(self.transactions[user])

            points_to_spend = min(points, transaction.points)
            self.point_totals[user][transaction.payer] -= points_to_spend
            points -= points_to_spend
            spent_points[transaction.payer] -= points_to_spend

            if transaction.points > points_to_spend:
                # If there are points leftover, put them back in the heap
                heapq.heappush(self.transactions[user], Transaction(transaction.payer, transaction.points - points_to_spend, transaction.timestamp))
        return spent_points

    @db_error_handler
    def get_points(self, user: str) -> Dict[str, int]:
        """
        Gets the point balances for each payer for the given user.

        Args:
            user (str): The user to get the point balances for.

        Returns:
            Dict[str, int]: Point balances for each payer for the given user.

        Raises:
            DatabaseException: If the user does not exist.
        """
        self.check_user_exists(user)
        return self.point_totals[user]

    @db_error_handler
    def get_total_points(self, user: str) -> int:
        """
        Gets the total number of points for the given user.

        Args:
            user (str): The user to get the total points for.

        Returns:
            int: The total number of points for the given user.

        Raises:
            DatabaseException: If the user does not exist.
        """
        self.check_user_exists(user)
        return sum([points for points in self.point_totals[user].values()])

    def check_user_exists(self, user):
        """
        Checks if the given user exists.

        Args:
            user (_type_): The user

        Raises:
            DatabaseException: If the user does not exist.
        """
        if user not in self.users:
            raise DatabaseException(f'User {user} does not exist')
