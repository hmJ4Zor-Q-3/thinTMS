import binascii

from flask import Response, jsonify, make_response

from src.database.user_access import IUserAccess
from src.database.user_database_manager import UserDatabaseManager
from src.routes.auth_routes import UserApi
from src.routes.implementation.auth_implementations import IUserApiImpl
from src.routes.status_codes import StatusCodes
from src.routes.validators import UserValidator
from src.security.security import ISecurityStandard


class TMSUserApiImpl(IUserApiImpl):
    """
    The user api implementation for the task management system.
    """

    def __init__(self, user_access: IUserAccess, security_standard: ISecurityStandard):
        self._ua = user_access
        self._ss = security_standard

        self._uv = UserValidator(self._ua)

    def auth(self, username: str, password: str) -> Response:
        h = self._ss.hash(password)
        r = self._uv.validate_login(username, h)
        if isinstance(r, Response):
            return r

        t = self._ua.login(username, h)
        return jsonify({UserApi.AUTH_TOKEN_KEY: str(binascii.hexlify(t))})

    def logout(self, username: str, token: str) -> Response:
        token = self._uv.validate_session(username, token)
        if isinstance(token, Response):
            return token

        self._ua.logout(username, token)
        return Response()

    def register(self, username: str, password: str) -> Response:
        if len(username) > UserDatabaseManager.USERNAME_LENGTH:
            r = make_response(f"Username's too long, max length is: {UserDatabaseManager.USERNAME_LENGTH}")
            r.status_code = StatusCodes.BAD_REQUEST
            return r

        if self._ua.is_user_registered(username):
            r = make_response("User already used.")
            r.status_code = StatusCodes.INVALID_USERNAME
            return r

        if not self._ss.is_password_valid(password):
            r = make_response("Password too weak.")
            r.status_code = StatusCodes.INVALID_PASSWORD
            return r

        t = self._ua.register_user(username, self._ss.hash(password))
        return jsonify({UserApi.AUTH_TOKEN_KEY: str(binascii.hexlify(t))})
