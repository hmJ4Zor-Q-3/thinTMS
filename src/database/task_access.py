from abc import ABC, abstractmethod

from src.data.task import Task
from src.data.unidentified_task import UnIDTask


class ITaskAccess(ABC):
    @abstractmethod
    def add_task(self, task: UnIDTask) -> Task:
        """
        Add's a given task to the system.
        Args:
            task:

        Returns:
            The task data and associated unique identifier.

        Raises:
            KeyError: Group isn't registered.
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: int) -> None:
        """
        Deletes a given task from the system.
        Args:
            task_id:

        Returns:

        Raises:
            KeyError: Task isn't registered.
        """
        pass

    @abstractmethod
    def get_task(self, task_id: int) -> Task:
        """
        Gets a given task from the system,
        Args:
            task_id:

        Returns:

        Raises:
            KeyError: Task isn't registered.

        """
        pass

    @abstractmethod
    def get_tasks(self, group_id: int) -> list[Task]:
        """
        Get's all the task's associated with the given group.
        Args:
            group_id:

        Returns:

        Raises:
            KeyError: Group isn't registered.
        """
        pass

    @abstractmethod
    def update_task(self, task: Task) -> None:
        """
        Update the task in the system that has the same identifier.
        Args:
            task:

        Returns:

        Raises:
            KeyError: Task isn't registered.
        """
        pass

    @abstractmethod
    def is_task_registered(self, task_id: int) -> bool:
        """
        Tests if a task's registered
        Args:
            task_id:

        Returns:

        """
        pass
