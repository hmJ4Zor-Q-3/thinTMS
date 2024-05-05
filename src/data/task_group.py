from src.data.unidentified_task_group import UnIDTaskGroup


class TaskGroup(UnIDTaskGroup):
    def __init__(self, username: str, name: str, identifier: int):
        super().__init__(username, name)
        self.identifier = identifier

    def __eq__(self, other):
        return (isinstance(other, TaskGroup)
                and super().__eq__(other)
                and (self.identifier == other.identifier))

    @classmethod
    def of(cls, base: UnIDTaskGroup, identifier: int):
        return TaskGroup(base.username, base.name, identifier)
