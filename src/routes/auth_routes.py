from flask import Blueprint, request

from src.routes.flask_routes import IFlaskRoutes
from src.routes.implementation.auth_implementations import IUserApiImpl


class UserApi(IFlaskRoutes):
    """
    Defines routes for managing a user and their session.
    """

    AUTH_TOKEN_KEY = "token"
    PASSWORD_KEY = "password"
    USERNAME_KEY = "username"

    AUTH_ENDPOINT_PATH = "/api/auth"
    LOGOUT_ENDPOINT_PATH = "/api/logout"
    REGISTER_ENDPOINT_PATH = "/api/register"

    def __init__(self, impl: IUserApiImpl):
        self.blueprint = Blueprint("api_endpoints", __name__)

        @self.blueprint.route(UserApi.AUTH_ENDPOINT_PATH)
        def auth():
            return impl.auth(request.args[UserApi.USERNAME_KEY], request.args[UserApi.PASSWORD_KEY])

        @self.blueprint.route(UserApi.LOGOUT_ENDPOINT_PATH)
        def logout():
            return impl.logout(request.args[UserApi.USERNAME_KEY], request.args[UserApi.AUTH_TOKEN_KEY])

        @self.blueprint.route(UserApi.REGISTER_ENDPOINT_PATH)
        def register():
            return impl.register(request.args[UserApi.USERNAME_KEY], request.args[UserApi.PASSWORD_KEY])

    def get_blueprint(self) -> Blueprint:
        return self.blueprint
