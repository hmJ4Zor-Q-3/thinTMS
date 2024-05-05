from abc import ABC, abstractmethod

from flask import Response


class ITaskApiImpl(ABC):

    @abstractmethod
    def get_task_groups(self, username: str, token: str) -> Response:
        """
        Gets a user's task groups, excluding their content.
        Args:
            username:
            token:

        Returns:

        """
        pass

    @abstractmethod
    def delete_task_group(self, username: str, token: str, group_id: str) -> Response:
        """
        Removes a group permanently from the system, or enqueues this to happen.
        Args:
            username:
            token:
            group_id:

        Returns:

        """
        pass

    @abstractmethod
    def get_task_group(self, username: str, token: str, group_id: str) -> Response:
        """
        Gets a task group's data, including a shortened view of it's tasks.
        Args:
            username:
            token:
            group_id:

        Returns:

        """
        pass

    @abstractmethod
    def post_task_group(self, username: str, token: str, group_id: str | None, name: str | None) -> Response:
        """
        Add a task group or updates a task group. If a group_id is given that task should then be updated,
        if it doesn't exist that's an error, no group_id means add new.

        Args:
            username:
            token:
            group_id:
            name:

        Returns:

        """
        pass

    @abstractmethod
    def delete_task(self, username: str, token: str, task_id: str) -> Response:
        """
        Removes a task permanently from the system, or enqueues this to happen.
        Args:
            username:
            token:
            task_id:

        Returns:

        """
        pass

    @abstractmethod
    def get_task(self, username: str, token: str, task_id: str) -> Response:
        """
        Gets all data on a given task.
        Args:
            username:
            token:
            task_id:

        Returns:

        """
        pass

    @abstractmethod
    def post_task(self, username: str, token: str, group_id: str | None, task_id: str | None, title: str | None,
                  description: str | None, due_date: str | None) -> Response:
        """
        Add or update a task. If a task_id is given that task should then be updated,
        if it doesn't exist that's an error, no task_id means add new.
        Args:
            group_id:
            username:
            token:
            task_id:
            title:
            description:
            due_date:

        Returns: the task_id if a new task's added.

        """
        pass
