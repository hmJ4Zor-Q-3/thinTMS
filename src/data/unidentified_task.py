from datetime import datetime
from typing import NamedTuple


class UnIDTask:
    def __init__(self, group_identifier: int, title: str, description: str, due_date: datetime | None):
        self.group_identifier = group_identifier
        self.title = title
        self.description = description
        self.due_date = due_date

    def __eq__(self, other):
        return (isinstance(other, UnIDTask)
                and (self.group_identifier == other.group_identifier)
                and (self.title == other.title)
                and (self.description == other.description)
                and (self.due_date == other.due_date))
