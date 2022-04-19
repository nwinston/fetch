from abc import abstractmethod, ABC
from typing import Dict

class Database(ABC):
    """
    Abstract interface for a database that can be used to store and retrieve
    user point totals and transactions.
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def add_transaction(self, user: str, payer: str, points: int, timestamp: str) -> None:
        """
        Adds a transaction to the database.

        Args:
            user (str): The user
            payer (str): The payer who is providing the points.
            points (int): The number of points being provided.
            timestamp (datetime.datetime): The timestamp of the transaction.
        """
        pass

    @abstractmethod
    def spend_points(self, user: str, points: int) -> None:
        """
        Spends points from the user's account.

        Args:
            user (str): The user spending points.
            points (int): The number of points to spend.
        """
        pass
    
    @abstractmethod
    def get_points(self, user: str) -> Dict[str, int]:
        """
        Gets the point balances for each payer for the given user.

        Args:
            user (str): The user to get the point balances for.

        Returns:
            Dict[str, int]: Point balances for each payer for the given user.
        """
        pass

    @abstractmethod
    def get_total_points(self, user: str) -> int:
        """
        Returns the total points for the given user.

        Args:
            user (str): The user

        Returns:
            int: Points for the given user
        """
        pass

    @abstractmethod
    def create_user(self, user: str) -> None:
        """
        Creates and regisiters a user to the database.

        Args:
            user (str): The user to create.
        """
        pass
    