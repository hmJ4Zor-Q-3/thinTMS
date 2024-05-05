from src.data.task import Task
from src.exceptions.invalid_state_error import InvalidStateError
from src.routes.task_routes import TaskApi


class TaskSerializer:
    def __init__(self):
        self.task = None  # type: Task

        self._identifier = True
        self._group_identifier = True
        self._description = True

    def start(self, task: Task):
        if self.task is not None:
            raise InvalidStateError("Builder already open.")

        self.task = task
        return self

    def drop_identifier(self):
        self._identifier = False
        return self

    def drop_group_identifier(self):
        self._group_identifier = False
        return self

    def drop_description(self):
        self._description = False
        return self

    def end(self) -> dict:
        # TODO, dont add any empty strings, they can just be inferred.
        d = {}
        if self._group_identifier:
            d[TaskApi.GROUP_ID_KEY] = self.task.group_identifier

        d[TaskApi.TASK_TITLE_KEY] = self.task.title

        if self._description:
            d[TaskApi.TASK_DESCRIPTION_KEY] = self.task.description

        if self.task.due_date is not None:
            d[TaskApi.TASK_DATE_KEY] = self.task.due_date.isoformat()

        if self._identifier:
            d[TaskApi.TASK_ID_KEY] = self.task.identifier

        self.reset()
        return d

    def reset(self):
        self.task = None

        self._identifier = True
        self._group_identifier = True
        self._description = True
