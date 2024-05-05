from unittest.mock import Mock

import pytest

from src.data.task_group import TaskGroup


class TaskGroupAccessUsingTest:
    GROUP_1 = 1
    GROUP_2 = 9
    GROUP_3 = 8
    UNUSED_ID = 2930
    GROUPS = [GROUP_1, GROUP_2, GROUP_3]

    ADD_RESULT_1 = TaskGroup("", "f&*Vu7ccy46xy", 1)
    ADD_RESULT_2 = TaskGroup("eytjhyyjjnyu6", "", 2)
    DELETE_RESULT_1 = 3
    DELETE_RESULT_2 = 4
    GET_RESULT_1 = TaskGroup("un", "Name", 129)
    GET_RESULT_2 = TaskGroup("f", "Title kind of", 0)
    GETS_RESULT_1 = [TaskGroup("f", "", 7), TaskGroup("03,_", "", 8), TaskGroup("0934", "Titles", 9)]
    GETS_RESULT_2 = [TaskGroup("usernameTheat,c93l", "Add new titles.", 24)]
    UPDATE_RESULT_1 = 5
    UPDATE_RESULT_2 = 6

    @pytest.fixture
    def task_group_access(self):
        """
            Creates a mock of an ITaskGroupAccess implementation.
            Returns:

        """
        tg_mock = Mock()
        tg_mock.add_task_group = Mock(side_effect=[TaskGroupAccessUsingTest.ADD_RESULT_1,
                                                   TaskGroupAccessUsingTest.ADD_RESULT_2])
        tg_mock.delete_task_group = Mock(side_effect=[TaskGroupAccessUsingTest.DELETE_RESULT_1,
                                                      TaskGroupAccessUsingTest.DELETE_RESULT_2])
        tg_mock.get_task_group = Mock(side_effect=[TaskGroupAccessUsingTest.GET_RESULT_1,
                                                   TaskGroupAccessUsingTest.GET_RESULT_2])
        tg_mock.get_task_groups = Mock(side_effect=[TaskGroupAccessUsingTest.GETS_RESULT_1,
                                                    TaskGroupAccessUsingTest.GETS_RESULT_2])
        tg_mock.update_task_group = Mock(side_effect=[TaskGroupAccessUsingTest.UPDATE_RESULT_1,
                                                      TaskGroupAccessUsingTest.UPDATE_RESULT_2])
        tg_mock.is_group_registered = lambda i: i in TaskGroupAccessUsingTest.GROUPS
        return tg_mock
