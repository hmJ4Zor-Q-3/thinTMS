from datetime import datetime

from src.data.unidentified_task import UnIDTask


class Task(UnIDTask):

    def __init__(self, group_identifier: int, title: str, description: str, due_date: datetime | None, identifier: int):
        super().__init__(group_identifier, title, description, due_date)
        self.identifier = identifier

    def __eq__(self, other):
        return (isinstance(other, Task)
                and super().__eq__(other)
                and (self.identifier == other.identifier))

    @classmethod
    def of(cls, task: UnIDTask, identifier: int):
        return Task(task.group_identifier, task.title, task.description, task.due_date, identifier)
