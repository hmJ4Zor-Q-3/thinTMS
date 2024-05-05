from flask import Blueprint, request

from src.routes.auth_routes import UserApi
from src.routes.flask_routes import IFlaskRoutes
from src.routes.implementation.task_implementation import ITaskApiImpl
from src.routes.methods import HTTPMethods


class TaskApi(IFlaskRoutes):
    """
    Defines routes for managing a user's tasks, and task groups.
    """

    GROUP_ID_KEY = "group_id"
    GROUP_NAME_KEY = "name"
    TASK_ID_KEY = "task_id"
    TASK_TITLE_KEY = "title"
    TASK_DESCRIPTION_KEY = "description"
    TASK_DATE_KEY = "date"

    TASK_GROUPS_ENDPOINT_PATH = "/api/task_groups"
    TASK_GROUP_ENDPOINT_PATH = "/api/task_group"
    TASK_ENDPOINT_PATH = "/api/task"

    def __init__(self, impl: ITaskApiImpl):
        self.blueprint = Blueprint("task_endpoints", __name__)

        @self.blueprint.route(TaskApi.TASK_GROUPS_ENDPOINT_PATH, methods=[HTTPMethods.GET_METHOD])
        def task_groups():
            return impl.get_task_groups(request.args[UserApi.USERNAME_KEY], request.args[UserApi.AUTH_TOKEN_KEY])

        @self.blueprint.route(TaskApi.TASK_GROUP_ENDPOINT_PATH,
                              methods=[HTTPMethods.DELETE_METHOD, HTTPMethods.GET_METHOD, HTTPMethods.POST_METHOD])
        def task_group():
            if request.method == HTTPMethods.DELETE_METHOD:
                return impl.delete_task_group(request.args[UserApi.USERNAME_KEY], request.args[UserApi.AUTH_TOKEN_KEY],
                                              request.args[TaskApi.GROUP_ID_KEY])
            elif request.method == HTTPMethods.GET_METHOD:
                return impl.get_task_group(request.args[UserApi.USERNAME_KEY], request.args[UserApi.AUTH_TOKEN_KEY],
                                           request.args[TaskApi.GROUP_ID_KEY])
            elif request.method == HTTPMethods.POST_METHOD:
                return impl.post_task_group(request.args[UserApi.USERNAME_KEY], request.args[UserApi.AUTH_TOKEN_KEY],
                                            request.args.get(TaskApi.GROUP_ID_KEY, None),
                                            request.args.get(TaskApi.GROUP_NAME_KEY, None))

        @self.blueprint.route(TaskApi.TASK_ENDPOINT_PATH,
                              methods=[HTTPMethods.DELETE_METHOD, HTTPMethods.GET_METHOD, HTTPMethods.POST_METHOD])
        def task():
            if request.method == HTTPMethods.DELETE_METHOD:
                return impl.delete_task(request.args[UserApi.USERNAME_KEY], request.args[UserApi.AUTH_TOKEN_KEY],
                                        request.args[TaskApi.TASK_ID_KEY])
            elif request.method == HTTPMethods.GET_METHOD:
                return impl.get_task(request.args[UserApi.USERNAME_KEY], request.args[UserApi.AUTH_TOKEN_KEY],
                                     request.args[TaskApi.TASK_ID_KEY])
            elif request.method == HTTPMethods.POST_METHOD:
                return impl.post_task(request.args[UserApi.USERNAME_KEY], request.args[UserApi.AUTH_TOKEN_KEY],
                                      request.args.get(TaskApi.GROUP_ID_KEY, None),
                                      request.args.get(TaskApi.TASK_ID_KEY, None),
                                      request.args.get(TaskApi.TASK_TITLE_KEY, None),
                                      request.args.get(TaskApi.TASK_DESCRIPTION_KEY, None),
                                      request.args.get(TaskApi.TASK_DATE_KEY, None))

    def get_blueprint(self) -> Blueprint:
        return self.blueprint
