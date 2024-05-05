import binascii

import pytest

from src.routes.implementation.tms_task_implementation import TMSTaskApiImpl
from src.routes.status_codes import StatusCodes
from src.test.util.task_access_using_test import TaskAccessUsingTest
from src.test.util.task_group_access_using_test import TaskGroupAccessUsingTest
from src.test.util.test_util import FlaskTest
from src.test.util.user_access_using_test import UserAccessUsingTest


class TestTMSTaskApiImpl(FlaskTest, UserAccessUsingTest, TaskGroupAccessUsingTest, TaskAccessUsingTest):

    @pytest.fixture
    def impl(self, user_access, task_group_access, task_access):
        """
        Generates a TMSTaskApiImpl.
        Args:
            user_access:
            task_group_access:
            task_access:

        Returns:

        """
        i = TMSTaskApiImpl(user_access, task_group_access, task_access)
        return i

    @pytest.mark.parametrize("username, token, expected_code, method_expectation", [
        (UserAccessUsingTest.UNUSED_USERNAME, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
         StatusCodes.INVALID_USERNAME, TaskGroupAccessUsingTest.GETS_RESULT_1),  # test bad username
        (UserAccessUsingTest.USERNAME_3, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
         StatusCodes.UNAUTHORIZED, TaskGroupAccessUsingTest.GETS_RESULT_1),  # test bad token
        (UserAccessUsingTest.USERNAME_1, "skrelk",
         StatusCodes.UNAUTHORIZED, TaskGroupAccessUsingTest.GETS_RESULT_1),  # test unreadable token
        (UserAccessUsingTest.USERNAME_1, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
         StatusCodes.SUCCESS, TaskGroupAccessUsingTest.GETS_RESULT_2)  # test valid request
    ])
    def test_get_task_groups(self, app_context, impl, username, token, expected_code, method_expectation):
        r = impl.get_task_groups(username, token)
        assert r.status_code == expected_code
        assert impl._tga.get_task_groups() == method_expectation

    @pytest.mark.parametrize("username, token, group_id, expected_code, method_expectation", [
        (UserAccessUsingTest.UNUSED_USERNAME, binascii.hexlify(UserAccessUsingTest.TOKEN_3),
         str(TaskGroupAccessUsingTest.GROUP_1),
         StatusCodes.INVALID_USERNAME, TaskGroupAccessUsingTest.DELETE_RESULT_1),  # test bad username
        (UserAccessUsingTest.USERNAME_3, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
         str(TaskGroupAccessUsingTest.GROUP_1),
         StatusCodes.UNAUTHORIZED, TaskGroupAccessUsingTest.DELETE_RESULT_1),  # test bad token
        (UserAccessUsingTest.USERNAME_1, "skrelk", str(TaskGroupAccessUsingTest.GROUP_1),
         StatusCodes.UNAUTHORIZED, TaskGroupAccessUsingTest.DELETE_RESULT_1),  # test unreadable token
        (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2), "1s2",
         StatusCodes.INVALID_IDENTIFIER, TaskGroupAccessUsingTest.DELETE_RESULT_1),  # test unreadable identifier
        (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
         str(TaskGroupAccessUsingTest.GROUP_3),
         StatusCodes.SUCCESS, TaskGroupAccessUsingTest.DELETE_RESULT_2)  # test valid request
    ])
    def test_delete_task_group(self, app_context, impl, username, token, group_id, expected_code, method_expectation):
        r = impl.delete_task_group(username, token, group_id)
        assert r.status_code == expected_code
        assert impl._tga.delete_task_group() == method_expectation

    @pytest.mark.parametrize("username, token, group_id, expected_code, get_group_expectation, get_tasks_expectation",
                             [
                                 (UserAccessUsingTest.UNUSED_USERNAME, binascii.hexlify(UserAccessUsingTest.TOKEN_3),
                                  str(TaskGroupAccessUsingTest.GROUP_1), StatusCodes.INVALID_USERNAME,
                                  TaskGroupAccessUsingTest.GET_RESULT_1, TaskAccessUsingTest.GETS_RESULT_1),
                                 # test bad username
                                 (UserAccessUsingTest.USERNAME_3, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
                                  str(TaskGroupAccessUsingTest.GROUP_1), StatusCodes.UNAUTHORIZED,
                                  TaskGroupAccessUsingTest.GET_RESULT_1, TaskAccessUsingTest.GETS_RESULT_1),
                                 # test bad token
                                 (UserAccessUsingTest.USERNAME_1, "skrelk", str(TaskGroupAccessUsingTest.GROUP_1),
                                  StatusCodes.UNAUTHORIZED, TaskGroupAccessUsingTest.GET_RESULT_1,
                                  TaskAccessUsingTest.GETS_RESULT_1),  # test unreadable token
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2), "1s2",
                                  StatusCodes.INVALID_IDENTIFIER, TaskGroupAccessUsingTest.GET_RESULT_1,
                                  TaskAccessUsingTest.GETS_RESULT_1),  # test unreadable identifier
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  str(TaskGroupAccessUsingTest.GROUP_3), StatusCodes.SUCCESS,
                                  TaskGroupAccessUsingTest.GET_RESULT_2, TaskAccessUsingTest.GETS_RESULT_2)
                                 # test valid request
                             ])
    def test_get_task_group(self, app_context, impl, username, token, group_id, expected_code, get_group_expectation,
                            get_tasks_expectation):
        r = impl.get_task_group(username, token, group_id)
        assert r.status_code == expected_code
        assert impl._tga.get_task_group() == get_group_expectation
        assert impl._ta.get_tasks() == get_tasks_expectation

    @pytest.mark.parametrize("username, token, group_id, name, expected_code, add_expectation, update_expectation",
                             [
                                 (UserAccessUsingTest.UNUSED_USERNAME, binascii.hexlify(UserAccessUsingTest.TOKEN_3),
                                  None, "New", StatusCodes.INVALID_USERNAME, TaskGroupAccessUsingTest.ADD_RESULT_1,
                                  TaskGroupAccessUsingTest.UPDATE_RESULT_1),  # test bad username
                                 (UserAccessUsingTest.USERNAME_3, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
                                  str(TaskGroupAccessUsingTest.GROUP_1), "", StatusCodes.UNAUTHORIZED,
                                  TaskGroupAccessUsingTest.ADD_RESULT_1, TaskGroupAccessUsingTest.UPDATE_RESULT_1),
                                 # test bad token
                                 (UserAccessUsingTest.USERNAME_1, "skrelk", str(TaskGroupAccessUsingTest.GROUP_2),
                                  "name", StatusCodes.UNAUTHORIZED, TaskGroupAccessUsingTest.ADD_RESULT_1,
                                  TaskGroupAccessUsingTest.UPDATE_RESULT_1),  # test unreadable token

                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2), "n",
                                  "Group name", StatusCodes.INVALID_IDENTIFIER, TaskGroupAccessUsingTest.ADD_RESULT_1,
                                  TaskGroupAccessUsingTest.UPDATE_RESULT_1),  # test unreadable identifier
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  str(TaskGroupAccessUsingTest.UNUSED_ID), "l", StatusCodes.INVALID_IDENTIFIER,
                                  TaskGroupAccessUsingTest.ADD_RESULT_1, TaskGroupAccessUsingTest.UPDATE_RESULT_1),
                                 # test nonexistent group

                                 (UserAccessUsingTest.USERNAME_3, binascii.hexlify(UserAccessUsingTest.TOKEN_3), None,
                                  "tezt", StatusCodes.SUCCESS, TaskGroupAccessUsingTest.ADD_RESULT_2,
                                  TaskGroupAccessUsingTest.UPDATE_RESULT_1),  # test valid request
                                 (UserAccessUsingTest.USERNAME_1, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
                                  str(TaskGroupAccessUsingTest.GROUP_2), "the title of the group", StatusCodes.SUCCESS,
                                  TaskGroupAccessUsingTest.ADD_RESULT_1, TaskGroupAccessUsingTest.UPDATE_RESULT_2)
                                 # test valid request

                             ])
    def test_post_task_group(self, app_context, impl, username, token, group_id, name, expected_code, add_expectation,
                             update_expectation):
        r = impl.post_task_group(username, token, group_id, name)
        assert r.status_code == expected_code
        assert impl._tga.add_task_group() == add_expectation
        assert impl._tga.update_task_group() == update_expectation

    @pytest.mark.parametrize("username, token, task_id, expected_code, method_expectation",
                             [
                                 (UserAccessUsingTest.UNUSED_USERNAME, binascii.hexlify(UserAccessUsingTest.TOKEN_3),
                                  str(TaskAccessUsingTest.TASK_2), StatusCodes.INVALID_USERNAME,
                                  TaskAccessUsingTest.DELETE_RESULT_1),  # test bad username
                                 (UserAccessUsingTest.USERNAME_3, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
                                  str(TaskAccessUsingTest.TASK_1), StatusCodes.UNAUTHORIZED,
                                  TaskAccessUsingTest.DELETE_RESULT_1),  # test bad token
                                 (UserAccessUsingTest.USERNAME_1, "skrelk", str(TaskAccessUsingTest.TASK_3),
                                  StatusCodes.UNAUTHORIZED, TaskAccessUsingTest.DELETE_RESULT_1),
                                 # test unreadable token
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2), "n",
                                  StatusCodes.INVALID_IDENTIFIER, TaskAccessUsingTest.DELETE_RESULT_1),
                                 # test unreadable identifier
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  str(TaskAccessUsingTest.UNUSED_ID), StatusCodes.INVALID_IDENTIFIER,
                                  TaskAccessUsingTest.DELETE_RESULT_1),  # test nonexistent task
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  str(TaskAccessUsingTest.TASK_1), StatusCodes.SUCCESS,
                                  TaskAccessUsingTest.DELETE_RESULT_2)  # test valid request
                             ])
    def test_delete_task(self, app_context, impl, username, token, task_id, expected_code, method_expectation):
        r = impl.delete_task(username, token, task_id)
        assert r.status_code == expected_code
        assert impl._ta.delete_task() == method_expectation

    @pytest.mark.parametrize("username, token, task_id, expected_code, method_expectation",
                             [
                                 (UserAccessUsingTest.UNUSED_USERNAME, binascii.hexlify(UserAccessUsingTest.TOKEN_3),
                                  str(TaskAccessUsingTest.TASK_2), StatusCodes.INVALID_USERNAME,
                                  TaskAccessUsingTest.GET_RESULT_1),  # test bad username
                                 (UserAccessUsingTest.USERNAME_3, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
                                  str(TaskAccessUsingTest.TASK_1), StatusCodes.UNAUTHORIZED,
                                  TaskAccessUsingTest.GET_RESULT_1),  # test bad token
                                 (UserAccessUsingTest.USERNAME_1, "skrelk", str(TaskAccessUsingTest.TASK_3),
                                  StatusCodes.UNAUTHORIZED, TaskAccessUsingTest.GET_RESULT_1),  # test unreadable token
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2), "n",
                                  StatusCodes.INVALID_IDENTIFIER, TaskAccessUsingTest.GET_RESULT_1),
                                 # test unreadable identifier
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  str(TaskAccessUsingTest.UNUSED_ID), StatusCodes.INVALID_IDENTIFIER,
                                  TaskAccessUsingTest.GET_RESULT_1),  # test nonexistent task
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  str(TaskAccessUsingTest.TASK_1), StatusCodes.SUCCESS,
                                  TaskAccessUsingTest.GET_RESULT_2)  # test valid request
                             ])
    def test_get_task(self, app_context, impl, username, token, task_id, expected_code, method_expectation):
        r = impl.get_task(username, token, task_id)
        assert r.status_code == expected_code
        assert impl._ta.get_task() == method_expectation

    @pytest.mark.parametrize("username, token, group_id, task_id, title, description, due_date, expected_code, "
                             "add_expectation, update_expectation",
                             [
                                 (UserAccessUsingTest.USERNAME_2, UserAccessUsingTest.TOKEN_2,
                                  TaskGroupAccessUsingTest.GROUP_2, TaskAccessUsingTest.TASK_2, "title", "desc", "date",
                                  StatusCodes.MISFORMATTED_DATE, TaskAccessUsingTest.ADD_RESULT_1,
                                  TaskAccessUsingTest.UPDATE_RESULT_1),  # test unparseable date
                                 (UserAccessUsingTest.USERNAME_2, UserAccessUsingTest.TOKEN_1,
                                  TaskGroupAccessUsingTest.GROUP_3, TaskAccessUsingTest.TASK_2, "title", "desc",
                                  "0030-09-09T33:23:13Z", StatusCodes.MISFORMATTED_DATE,
                                  TaskAccessUsingTest.ADD_RESULT_1, TaskAccessUsingTest.UPDATE_RESULT_1),
                                 # test unreal date

                                 (UserAccessUsingTest.UNUSED_USERNAME, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
                                  TaskGroupAccessUsingTest.GROUP_3, TaskAccessUsingTest.TASK_2, "title", "desc",
                                  "2230-11-09T08:23:13Z", StatusCodes.INVALID_USERNAME,
                                  TaskAccessUsingTest.ADD_RESULT_1, TaskAccessUsingTest.UPDATE_RESULT_1),
                                 # test unregistered username
                                 (UserAccessUsingTest.USERNAME_2, UserAccessUsingTest.TOKEN_1,
                                  str(TaskGroupAccessUsingTest.GROUP_3), TaskAccessUsingTest.TASK_2, "titl", "desc", None,
                                  StatusCodes.UNAUTHORIZED, TaskAccessUsingTest.ADD_RESULT_1,
                                  TaskAccessUsingTest.UPDATE_RESULT_1),  # test unparseable token
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
                                  str(TaskGroupAccessUsingTest.GROUP_3), TaskAccessUsingTest.TASK_3, "aswd", "dwsa", None,
                                  StatusCodes.UNAUTHORIZED, TaskAccessUsingTest.ADD_RESULT_1,
                                  TaskAccessUsingTest.UPDATE_RESULT_1),  # test wrong token

                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  "34l34ddd", str(TaskAccessUsingTest.TASK_3), "aswd", "", None,
                                  StatusCodes.INVALID_IDENTIFIER, TaskAccessUsingTest.ADD_RESULT_1,
                                  TaskAccessUsingTest.UPDATE_RESULT_1),  # test unparseable group_id
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  str(TaskGroupAccessUsingTest.UNUSED_ID), str(TaskAccessUsingTest.TASK_3), "aswd",
                                  None, "0001-01-01T01:00:00Z", StatusCodes.INVALID_IDENTIFIER,
                                  TaskAccessUsingTest.ADD_RESULT_1, TaskAccessUsingTest.UPDATE_RESULT_1),
                                 # test unregisted group_id

                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  str(TaskGroupAccessUsingTest.GROUP_1), "", "", "None", None,
                                  StatusCodes.INVALID_IDENTIFIER, TaskAccessUsingTest.ADD_RESULT_1,
                                  TaskAccessUsingTest.UPDATE_RESULT_1),  # test unparseable task_id
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
                                  str(TaskGroupAccessUsingTest.GROUP_2), str(TaskAccessUsingTest.UNUSED_ID), "aswd",
                                  None, None, StatusCodes.INVALID_IDENTIFIER, TaskAccessUsingTest.ADD_RESULT_1,
                                  TaskAccessUsingTest.UPDATE_RESULT_1),  # test unregisted task_id

                                 (UserAccessUsingTest.USERNAME_1, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
                                  str(TaskGroupAccessUsingTest.GROUP_3), None, "aswd", "we", None, StatusCodes.SUCCESS,
                                  TaskAccessUsingTest.ADD_RESULT_2, TaskAccessUsingTest.UPDATE_RESULT_1),
                                 # test valid task add call
                                 (UserAccessUsingTest.USERNAME_3, binascii.hexlify(UserAccessUsingTest.TOKEN_3),
                                  str(TaskGroupAccessUsingTest.GROUP_2), str(TaskAccessUsingTest.TASK_1), "aswd", "",
                                  "9901-11-02T21:02:31Z", StatusCodes.SUCCESS, TaskAccessUsingTest.ADD_RESULT_1,
                                  TaskAccessUsingTest.UPDATE_RESULT_2),  # test valid task update call
                             ])
    def test_post_task(self, app_context, impl, username, token, group_id, task_id, title, description, due_date,
                       expected_code, add_expectation, update_expectation):
        r = impl.post_task(username, token, group_id, task_id, title, description, due_date)
        assert r.status_code == expected_code
        assert impl._ta.add_task() == add_expectation
        assert impl._ta.update_task() == update_expectation

    # TODO, test responses json format's're correct
