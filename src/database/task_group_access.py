from abc import abstractmethod, ABC

from src.data.task_group import TaskGroup
from src.data.unidentified_task_group import UnIDTaskGroup


class ITaskGroupAccess(ABC):
    @abstractmethod
    def add_task_group(self, task_group: UnIDTaskGroup) -> TaskGroup:
        """
        Add's the task group to the system.
        Args:
            task_group:

        Returns:
            The task group data and newly associated unique identifier.

        Raises:
            UsernameError: User isn't registered.

        """
        pass

    @abstractmethod
    def delete_task_group(self, group_id: int) -> None:
        """
        Deletes a task group from the system.
        Args:
            group_id:

        Returns:

        Raises:
            KeyError: Group isn't registered.
        """
        pass

    @abstractmethod
    def get_task_group(self, group_id: int) -> TaskGroup:
        """
        Get's a task group from the system.
        Args:
            group_id:

        Returns:

        Raises:
            KeyError: Group isn't registered.
        """
        pass

    @abstractmethod
    def get_task_groups(self, username: str) -> list[TaskGroup]:
        """
        Get's all the task groups associated with the user.
        Args:
            username:

        Returns:
            UsernameError: User isn't registered.
        """
        pass

    @abstractmethod
    def update_task_group(self, task_group: TaskGroup) -> None:
        """
        Update the task group in the system with a matching identifier.
        Args:
            task_group:

        Returns:

        Raises:
            KeyError: Group isn't registered.
        """
        pass

    @abstractmethod
    def is_group_registered(self, group_id: int) -> bool:
        """
        Tests if a given group's registered with the system.
        Args:
            group_id:

        Returns:

        """
        pass
