from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

from src.data.task import Task


class TaskAccessUsingTest:
    TASK_1 = 3
    TASK_2 = 1
    TASK_3 = 901
    UNUSED_ID = 21
    TASKS = [TASK_1, TASK_2, TASK_3]

    ADD_RESULT_1 = Task(0, "", "", None, 100)
    ADD_RESULT_2 = Task(0, "", "", None, 99)
    DELETE_RESULT_1 = 98
    DELETE_RESULT_2 = 76
    GET_RESULT_1 = Task(90, "Name", "", datetime.now(), 78)
    GET_RESULT_2 = Task(11, "", "Description", None, 921)
    GETS_RESULT_1 = [Task(75, "", "", None, 00), Task(73, "//", "/\\ /\\", datetime.now(), 902392), Task(71, "Titles", "desc", None, 22)]
    GETS_RESULT_2 = [Task(24, "Add new titles.", "We need new titles for our tasks that're more consisely descriptive",
                      datetime.now() + timedelta(hours=1), 1)]
    UPDATE_RESULT_1 = 77
    UPDATE_RESULT_2 = 50

    @pytest.fixture
    def task_access(self):
        """
        Creates a mock of an ITaskAccess implementation.
        Returns:

        """
        t_mock = Mock()

        t_mock.add_task = Mock(side_effect=[TaskAccessUsingTest.ADD_RESULT_1,
                                            TaskAccessUsingTest.ADD_RESULT_2])
        t_mock.delete_task = Mock(side_effect=[TaskAccessUsingTest.DELETE_RESULT_1,
                                               TaskAccessUsingTest.DELETE_RESULT_2])
        t_mock.get_task = Mock(side_effect=[TaskAccessUsingTest.GET_RESULT_1,
                                            TaskAccessUsingTest.GET_RESULT_2])
        t_mock.get_tasks = Mock(side_effect=[TaskAccessUsingTest.GETS_RESULT_1,
                                             TaskAccessUsingTest.GETS_RESULT_2])
        t_mock.update_task = Mock(side_effect=[TaskAccessUsingTest.UPDATE_RESULT_1,
                                               TaskAccessUsingTest.UPDATE_RESULT_2])

        t_mock.is_task_registered = lambda iden: iden in TaskAccessUsingTest.TASKS
        return t_mock
