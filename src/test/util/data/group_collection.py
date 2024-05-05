from typing import NamedTuple

from src.data.task_group import TaskGroup
from src.test.util.data.user import User


class GroupCollection(NamedTuple):
    users: list[User]
    groups: list[TaskGroup]
