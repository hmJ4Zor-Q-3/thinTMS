from flask import Response, jsonify, make_response

from src.data.serialization.json.task_serializer import TaskSerializer
from src.data.task import Task
from src.data.task_group import TaskGroup
from src.data.unidentified_task import UnIDTask
from src.data.unidentified_task_group import UnIDTaskGroup
from src.database.task_access import ITaskAccess
from src.database.task_database_manager import TaskDatabaseManager
from src.database.task_group_access import ITaskGroupAccess
from src.database.task_group_database_manager import TaskGroupDatabaseManager
from src.database.user_access import IUserAccess
from src.routes.implementation.task_implementation import ITaskApiImpl
from src.routes.status_codes import StatusCodes
from src.routes.task_routes import TaskApi
from src.routes.validators import UserValidator, TaskValidator, TaskGroupValidator, DateValidator


class TMSTaskApiImpl(ITaskApiImpl):

    def __init__(self, user_access: IUserAccess, task_group_access: ITaskGroupAccess, task_access: ITaskAccess):
        self._ua = user_access
        self._tga = task_group_access
        self._ta = task_access

        self._uv = UserValidator(user_access)
        self._tgv = TaskGroupValidator(task_group_access)
        self._tv = TaskValidator(task_access)
        self._dv = DateValidator()

        self._ts = TaskSerializer()

    def get_task_groups(self, username: str, token: str) -> Response:
        token = self._uv.validate_session(username, token)
        if isinstance(token, Response):
            return token

        d = self._tga.get_task_groups(username)
        json = [{TaskApi.GROUP_ID_KEY: t.identifier, TaskApi.GROUP_NAME_KEY: t.name} for t in d]
        for json_obj in json:
            if json_obj[TaskApi.GROUP_NAME_KEY] == "":
                del json_obj[TaskApi.GROUP_NAME_KEY]
        return jsonify(json)

    def delete_task_group(self, username: str, token: str, group_id: str) -> Response:
        token = self._uv.validate_session(username, token)
        if isinstance(token, Response):
            return token

        group_id = self._tgv.validate_group_id(group_id)
        if isinstance(group_id, Response):
            return group_id

        self._tga.delete_task_group(group_id)
        return Response()

    def get_task_group(self, username: str, token: str, group_id: str) -> Response:
        token = self._uv.validate_session(username, token)
        if isinstance(token, Response):
            return token

        group_id = self._tgv.validate_group_id(group_id)
        if isinstance(group_id, Response):
            return group_id

        return jsonify(
            {TaskApi.GROUP_NAME_KEY: self._tga.get_task_group(group_id).name,
             "contents": [self._ts.start(t).drop_group_identifier().drop_description().end() for t in self._ta.get_tasks(group_id)]})

    def post_task_group(self, username: str, token: str, group_id: str | None, name: str | None) -> Response:
        name = name if name is not None else ""
        if len(name) > TaskGroupDatabaseManager.NAME_LENGTH:
            r = make_response(f"Task group name's too long, max length is: {TaskGroupDatabaseManager.NAME_LENGTH}")
            r.status_code = StatusCodes.BAD_REQUEST
            return r

        token = self._uv.validate_session(username, token)
        if isinstance(token, Response):
            return token

        if group_id is not None:
            group_id = self._tgv.validate_group_id(group_id)
            if isinstance(group_id, Response):
                return group_id

        if group_id is None:
            tg = self._tga.add_task_group(UnIDTaskGroup(username, name))
            return jsonify({TaskApi.GROUP_ID_KEY: tg.identifier})
        else:
            self._tga.update_task_group(TaskGroup(username, name, group_id))
            return Response()

    def delete_task(self, username: str, token: str, task_id: str) -> Response:
        token = self._uv.validate_session(username, token)
        if isinstance(token, Response):
            return token

        task_id = self._tv.validate_task_id(task_id)
        if isinstance(task_id, Response):
            return task_id

        self._ta.delete_task(task_id)
        return Response()

    def get_task(self, username: str, token: str, task_id: str) -> Response:
        token = self._uv.validate_session(username, token)
        if isinstance(token, Response):
            return token

        task_id = self._tv.validate_task_id(task_id)
        if isinstance(task_id, Response):
            return task_id

        return jsonify(self._ts.start(self._ta.get_task(task_id)).drop_group_identifier().drop_identifier().end())

    def post_task(self, username: str, token: str, group_id: str | None, task_id: str | None, title: str | None,
                  description: str | None, due_date: str | None) -> Response:
        title = title if title is not None else ""
        if len(title) > TaskDatabaseManager.TITLE_LENGTH:
            r = make_response(f"Task title is too long, max length is: {TaskDatabaseManager.TITLE_LENGTH}")
            r.status_code = StatusCodes.BAD_REQUEST
            return r

        if task_id is None and group_id is None:
            r = make_response(f"group or task identifier required.")
            r.status_code = StatusCodes.BAD_REQUEST
            return r

        if due_date is not None:
            due_date = self._dv.validate_datetime(due_date)
            if isinstance(due_date, Response):
                return due_date

        token = self._uv.validate_session(username, token)
        if isinstance(token, Response):
            return token

        if group_id is not None:
            group_id = self._tgv.validate_group_id(group_id)
            if isinstance(group_id, Response):
                return group_id

        if task_id is not None:
            task_id = self._tv.validate_task_id(task_id)
            if isinstance(task_id, Response):
                return task_id

        description = description if description is not None else ""

        if task_id is None:
            t = self._ta.add_task(UnIDTask(group_id, title, description, due_date))
            return jsonify({TaskApi.TASK_ID_KEY: t.identifier})
        else:
            self._ta.update_task(Task(group_id, title, description, due_date, task_id))
            return Response()
