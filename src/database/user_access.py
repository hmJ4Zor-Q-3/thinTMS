from abc import ABC, abstractmethod


class IUserAccess(ABC):

    @abstractmethod
    def login(self, username: str, password_hash: bytes) -> bytes:
        """
        Opens a new session for the user.
        Args:
            username:
            password_hash:

        Returns:
            The authorization token.

        Raises:
            UsernameError: User isn't registered.
            PasswordError: Password doesn't match.
        """
        pass

    @abstractmethod
    def logout(self, username: str, auth_token: bytes) -> None:
        """
        Close the users current session.
        Args:
            username:
            auth_token:

        Returns:

        Raises:
            UsernameError: User isn't registered.
            AuthTokenError: Token doesn't match, including the user doesn't currently have an open session.
        """
        pass

    @abstractmethod
    def register_user(self, username: str, password_hash: bytes) -> bytes:
        """
        Record a new user in the system and logs them in by default.
        Args:
            username:
            password_hash:

        Returns:
            The authorization token for the user's session.

        Raises:
            UsernameError: Username already taken.
        """
        pass

    @abstractmethod
    def is_user_registered(self, username: str) -> bool:
        """
        Check if a given user's registered with the system.
        Args:
            username:

        Returns:

        """
        pass

    @abstractmethod
    def is_user_login(self, username: str, password_hash: bytes) -> bool:
        """
        Check if the login information matches what's stored in the system.
        Args:
            username:
            password_hash:

        Returns:

        Raises:
            UsernameError: User doesn't exist.
        """
        pass

    @abstractmethod
    def is_valid_session(self, username: str, token: bytes) -> bool:
        """
        Check is the session matches the user's current session.
        Args:
            username:
            token:

        Returns:

        Raises:
            UsernameError: User doesn't exist.
        """
        pass
