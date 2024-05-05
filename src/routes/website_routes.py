import os.path

from flask import Blueprint, render_template

from src.routes.flask_routes import IFlaskRoutes
from src.routes.methods import HTTPMethods


class TMSWebsiteRoutes(IFlaskRoutes):
    TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend/website/")
    STATIC_PATH = TEMPLATES_PATH

    HOMEPAGE_FILE_PATH = "homepage.html"
    HOMEPAGE_ROUTE = "/"

    WORKSPACE_FILE_PATH = "workspace.html"
    WORKSPACE_ROUTE = "/workspace"

    def __init__(self, max_username_length: int, min_password_length: int):
        self.blueprint = Blueprint("website", __name__)

        @self.blueprint.route(TMSWebsiteRoutes.HOMEPAGE_ROUTE, methods=[HTTPMethods.GET_METHOD])
        def homepage():
            return render_template(TMSWebsiteRoutes.HOMEPAGE_FILE_PATH,
                                   homepage_route=TMSWebsiteRoutes.HOMEPAGE_ROUTE,
                                   workspace_route=TMSWebsiteRoutes.WORKSPACE_ROUTE,
                                   var_max_username_length=max_username_length,
                                   password_min_length=min_password_length)

        @self.blueprint.route(TMSWebsiteRoutes.WORKSPACE_ROUTE, methods=[HTTPMethods.GET_METHOD])
        def workspace():
            return render_template(TMSWebsiteRoutes.WORKSPACE_FILE_PATH,
                                   homepage_route=TMSWebsiteRoutes.HOMEPAGE_ROUTE,
                                   workspace_route=TMSWebsiteRoutes.WORKSPACE_ROUTE,
                                   var_max_username_length=max_username_length,
                                   password_min_length=min_password_length)

    def get_blueprint(self) -> Blueprint:
        return self.blueprint
