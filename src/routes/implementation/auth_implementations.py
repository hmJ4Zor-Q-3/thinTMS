from abc import ABC, abstractmethod

from flask import Response


class IUserApiImpl(ABC):

    @abstractmethod
    def auth(self, username: str, password: str) -> Response:
        """
        Authenticate a username and password to log in to an account.
        Args:
            username: The user's username.
            password: The user's password.

        Returns: An auth token, or status codes that're an indication what went wrong.

        """
        pass

    @abstractmethod
    def logout(self, username: str, token: str) -> Response:
        """
        Closes out the current session.
        Args:
            username: The user's username.
            token: The users current auth token to close.

        Returns: Various status codes.

        """
        pass

    @abstractmethod
    def register(self, username: str, password: str) -> Response:
        """
        Add a new account to the server.
        Args:
            username: The user's username.
            password: The user's password.

        Returns: An auth token, or status codes that're an indication what went wrong.

        """
        pass
