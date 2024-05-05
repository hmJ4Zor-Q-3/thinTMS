import binascii
from datetime import datetime

from src.database.database_manager import DataBaseManager
from src.database.user_access import IUserAccess
from src.exceptions.exceptions import UsernameError, PasswordError, AuthTokenError
from src.security.security import ISecurityStandard


class UserDatabaseManager(DataBaseManager, IUserAccess):
    """A class to manage users stored in an SQLite database."""

    USER_TABLE_NAME = "users"
    USERNAME_COLUMN_NAME = "username"
    PASSWORD_COLUMN_NAME = "password"
    AUTH_TOKEN_COLUMN_NAME = "auth_token"
    TOKEN_EXPIRY_COLUMN_NAME = "token_expiry"

    USERNAME_LENGTH = 30

    def __init__(self, db_path: str, security_standard: ISecurityStandard):
        """Initialize UserManager with the path to the SQLite database."""
        super().__init__(db_path)
        self.security_standard = security_standard
        self._initialize_db()

    def _initialize_db(self):
        with self.connection():
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {UserDatabaseManager.USER_TABLE_NAME} ("
                f"{UserDatabaseManager.USERNAME_COLUMN_NAME} VARCHAR({UserDatabaseManager.USERNAME_LENGTH}) PRIMARY KEY, "
                f"{UserDatabaseManager.PASSWORD_COLUMN_NAME} TEXT NOT NULL, "
                f"{UserDatabaseManager.AUTH_TOKEN_COLUMN_NAME} TEXT,"
                f"{UserDatabaseManager.TOKEN_EXPIRY_COLUMN_NAME} TEXT)")

    def login(self, username: str, password_hash: bytes) -> bytes:
        if not self.is_user_login(username, password_hash):
            raise PasswordError(f"Password didn't match.")

        token = self.security_standard.create_auth_token()
        exp = self.security_standard.create_auth_token_expiry()
        self._set_user_session(username, token, exp)

        return token

    def logout(self, username: str, auth_token: bytes) -> None:
        if not self.is_valid_session(username, auth_token):
            raise AuthTokenError(f"Not valid session.")

        self._set_user_session(username, None, None)

    def register_user(self, username: str, password_hash: bytes) -> bytes:
        if self.is_user_registered(username):
            raise UsernameError("Username already taken")

        with self.connection():
            self.cursor.execute(f"INSERT INTO {UserDatabaseManager.USER_TABLE_NAME} "
                                f"({UserDatabaseManager.USERNAME_COLUMN_NAME}, "
                                f"{UserDatabaseManager.PASSWORD_COLUMN_NAME}) "
                                f"VALUES (?, ?)",
                                (username, binascii.hexlify(password_hash)))
            self.conn.commit()

        return self.login(username, password_hash)

    def is_user_registered(self, username: str) -> bool:
        with self.connection():
            return len(self.cursor.execute(f"SELECT {UserDatabaseManager.USERNAME_COLUMN_NAME} "
                                           f"FROM {UserDatabaseManager.USER_TABLE_NAME} "
                                           f"WHERE {UserDatabaseManager.USERNAME_COLUMN_NAME}=?", (username, ))
                       .fetchall()) == 1

    def is_user_login(self, username: str, password_hash: bytes) -> bool:
        if not self.is_user_registered(username):
            raise UsernameError(f"User: {username}, does not exist")

        with self.connection():
            return len(self.cursor.execute(f"SELECT {UserDatabaseManager.USERNAME_COLUMN_NAME} "
                                           f"FROM {UserDatabaseManager.USER_TABLE_NAME} "
                                           f"WHERE {UserDatabaseManager.USERNAME_COLUMN_NAME}=? "
                                           f"AND {UserDatabaseManager.PASSWORD_COLUMN_NAME}=?",
                                           (username, binascii.hexlify(password_hash)))
                       .fetchall()) == 1

    def is_valid_session(self, username: str, token: bytes) -> bool:
        if not self.is_user_registered(username):
            raise UsernameError(f"User: {username}, does not exist")

        with self.connection():
            return len(self.cursor.execute(f"SELECT {UserDatabaseManager.USERNAME_COLUMN_NAME} "
                                           f"FROM {UserDatabaseManager.USER_TABLE_NAME} "
                                           f"WHERE {UserDatabaseManager.USERNAME_COLUMN_NAME}=? "
                                           f"AND {UserDatabaseManager.AUTH_TOKEN_COLUMN_NAME}=?",
                                           (username, binascii.hexlify(token)))
                       .fetchall()) == 1

    def _set_user_session(self, username: str, auth_token: bytes | None, expiry: datetime | None):
        with self.connection():
            self.cursor.execute(f"UPDATE {UserDatabaseManager.USER_TABLE_NAME} "
                                f"SET {UserDatabaseManager.AUTH_TOKEN_COLUMN_NAME}=?, "
                                f"    {UserDatabaseManager.TOKEN_EXPIRY_COLUMN_NAME}=? "
                                f"WHERE {UserDatabaseManager.USERNAME_COLUMN_NAME}=?",
                                (binascii.hexlify(auth_token) if auth_token is not None else None,
                                 expiry.isoformat() if expiry is not None else None,
                                 username))
            self.conn.commit()
