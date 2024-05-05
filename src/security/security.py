import hashlib
import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class ISecurityStandard(ABC):
    """
         A class defining a security standard interface.
    """

    @abstractmethod
    def create_auth_token(self) -> bytes:
        """
            Generates a random auth token.
            Returns: The auth token as bytes.

        """
        pass

    @abstractmethod
    def create_auth_token_expiry(self) -> datetime:
        """
            Generates the time at which an auth token generated at the time of the call will expire.
            Returns: The expiry time.

        """
        pass

    @abstractmethod
    def hash(self, password: str) -> bytes:
        """
        Returns a hash of the given password
        Args:
            password: the password to be hashed

        Returns: the hashed password as bytes.

        """
        pass

    @abstractmethod
    def is_password_valid(self, password: str) -> bool:
        """
            Checks that a password matches security rules.
            Args:
                password: the password to be tested

            Returns: If the password is valid according to the rules.

        """
        pass


class TMSSecurityStandard(ISecurityStandard):
    """
    The security standard implementation for the task management system.
    """
    PASSWORD_MIN_LENGTH = 12
    AUTH_TOKEN_BYTES = 32
    AUTH_TOKEN_LIFESPAN_HOURS = 6

    def create_auth_token(self) -> bytes:
        """
        Generates a random 256 bit auth token.
        Returns: The auth token as bytes.

        """
        return random.randbytes(TMSSecurityStandard.AUTH_TOKEN_BYTES)

    def create_auth_token_expiry(self) -> datetime:
        """
        Generates a time six hours from now
        Returns:

        """
        return timedelta(hours=6) + datetime.now()

    def hash(self, password: str) -> bytes:
        """
        Returns a 256bit SHA hash of the given password
        Args:
            password: the password to be hashed

        Returns: the hashed password as bytes.

        """
        if not isinstance(password, str):
            raise TypeError("Only strings can be passwords.")

        return hashlib.sha256(password.encode(), usedforsecurity=True).digest()

    def is_password_valid(self, password: str) -> bool:
        """
        Checks that a password matches the rules: length >= PASSWORD_MIN_LENGTH, has a number, has a lowercase,
        has an uppercase, has a symbol.
        Args:
            password: the password to be tested

        Returns: If the password is valid according to the rules.

        """
        if not isinstance(password, str):
            raise TypeError("Only strings can be passwords.")

        return (self.is_password_valid_length(password)
                and self.password_has_number(password)
                and self.password_has_lowercase(password)
                and self.password_has_uppercase(password)
                and self.password_has_symbol(password))

    def is_password_valid_length(self, password: str) -> bool:
        return len(password) >= TMSSecurityStandard.PASSWORD_MIN_LENGTH

    def password_has_number(self, password: str):
        return any(char.isdigit() for char in password)

    def password_has_lowercase(self, password: str):
        return any(char.islower() for char in password)

    def password_has_uppercase(self, password: str):
        return any(char.isupper() for char in password)

    def password_has_symbol(self, password: str):
        return any(not char.isalnum() for char in password)