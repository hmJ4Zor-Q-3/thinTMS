import binascii
from datetime import datetime

from flask import Response, make_response

from src.database.task_access import ITaskAccess
from src.database.task_group_access import ITaskGroupAccess
from src.database.user_access import IUserAccess
from src.routes.status_codes import StatusCodes


class UserValidator:
    """
        Utility class for parsing a user session, or preparing a response if they're invalid.
    """

    def __init__(self, user_access: IUserAccess):
        self._ua = user_access

    def validate_session(self, username: str, token: str) -> Response | bytes:
        """
        Checks a session for validity.
        Args:
            username:
            token:

        Returns: None if valid, otherwise a response detailing what went wrong.

        """
        try:
            token = binascii.unhexlify(token)
        except binascii.Error:
            r = make_response("Token not readable")
            r.status_code = StatusCodes.UNAUTHORIZED
            return r

        r = self.validate_username(username)
        if isinstance(r, Response):
            return r

        if not self._ua.is_valid_session(username, token):
            r = make_response("Token not valid")
            r.status_code = StatusCodes.UNAUTHORIZED
            return r

        return token

    def validate_username(self, username: str) -> Response | None:
        if not self._ua.is_user_registered(username):
            r = make_response("User not found")
            r.status_code = StatusCodes.INVALID_USERNAME
            return r

    def validate_login(self, username: str, password_hash: bytes) -> Response | None:
        r = self.validate_username(username)
        if isinstance(r, Response):
            return r

        if not self._ua.is_user_login(username, password_hash):
            r = make_response("Password was wrong.")
            r.status_code = StatusCodes.INVALID_PASSWORD
            return r


class TaskGroupValidator:
    """
        Utility class for parsing task group identifiers, or preparing a response if they're invalid.
    """

    def __init__(self, task_group_access: ITaskGroupAccess):
        self._tga = task_group_access

    def validate_group_id(self, group_id: str) -> Response | int:
        """
        Check if the task group id string is formatted as expected. And if it's a group that exists.
        Args:
            group_id:

        Returns: A response if an error occured detailing the error, otherwise the now parsed value.

        """
        try:
            group_id = int(group_id)
            if not self._tga.is_group_registered(group_id):
                raise ValueError
        except ValueError:
            token = make_response("Invalid group identifier.")
            token.status_code = StatusCodes.INVALID_IDENTIFIER
            return token

        return group_id


class TaskValidator:
    """
        Utility class for parsing a task identifier, or preparing a response if they're invalid.
    """

    def __init__(self, task_access: ITaskAccess):
        self._ta = task_access

    def validate_task_id(self, task_id: str) -> Response | int:
        """
        Check if the task id is formatted as expected. And if it's a task that exists.
        Args:
            task_id:

        Returns: A response if an error occured detailing the error, otherwise the now parsed value.

        """
        try:
            task_id = int(task_id)
            if not self._ta.is_task_registered(task_id):
                raise ValueError
        except ValueError:
            token = make_response("Invalid task identifier.")
            token.status_code = StatusCodes.INVALID_IDENTIFIER
            return token

        return task_id


class DateValidator:
    """
    Utility class for parsing datetimes, or preparing a response if they're invalid.
    """

    def validate_datetime(self, date: str) -> Response | datetime:
        """
        Check if the date string is formatted as expected.
        Args:
            date:

        Returns: A response if an error occured detailing the error, otherwise the now parsed value.

        """
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            token = make_response("Unreadable date format, use ISO 8601.")
            token.status_code = StatusCodes.MISFORMATTED_DATE
            return token

        return date
