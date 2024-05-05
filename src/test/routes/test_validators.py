import binascii
from datetime import datetime, timezone

import pytest
from flask import Response

from src.routes.status_codes import StatusCodes
from src.routes.validators import DateValidator, UserValidator, TaskGroupValidator, TaskValidator
from src.test.util.task_access_using_test import TaskAccessUsingTest
from src.test.util.task_group_access_using_test import TaskGroupAccessUsingTest
from src.test.util.test_util import FlaskTest
from src.test.util.user_access_using_test import UserAccessUsingTest


class TestDateValidator(FlaskTest):

    @pytest.fixture
    def validator(self):
        return DateValidator()

    @pytest.mark.parametrize("date, expectation",
                             [("s", StatusCodes.MISFORMATTED_DATE),  # test an input that's not a date
                              ("20240317T190939Z",  # test a date that's valid
                               datetime(2024, 3, 17, 19, 9, 39, tzinfo=timezone.utc)),
                              ("1802-12-31T03:00:52Z",  # test a date that's valid
                               datetime(1802, 12, 31, 3, 0, 52, tzinfo=timezone.utc)),
                              ("1802-12-32T03:00:52Z", StatusCodes.MISFORMATTED_DATE)
                              # test input that's not a real date
                              ])
    def test_validate_datetime(self, app_context, validator, date, expectation):
        r = validator.validate_datetime(date)
        if isinstance(r, Response):
            assert r.status_code == expectation
        else:
            assert r == expectation


class TestUserValidator(FlaskTest, UserAccessUsingTest):

    @pytest.fixture
    def validator(self, user_access):
        return UserValidator(user_access)

    @pytest.mark.parametrize("username, token, expectation", [
        (UserAccessUsingTest.USERNAME_1, binascii.hexlify(UserAccessUsingTest.TOKEN_2), StatusCodes.UNAUTHORIZED),
        # test token doesn't match user
        (UserAccessUsingTest.USERNAME_3, "3IFE", StatusCodes.UNAUTHORIZED),  # test unparseable token
        (UserAccessUsingTest.UNUSED_USERNAME, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
         StatusCodes.INVALID_USERNAME),  # test username that doesn't exist
        (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_2),
         UserAccessUsingTest.TOKEN_2)])  # test valid login
    def test_validate_session(self, app_context, validator, username, token, expectation):
        r = validator.validate_session(username, token)
        if isinstance(r, Response):
            assert r.status_code == expectation
        else:
            assert r == expectation

    @pytest.mark.parametrize("username, expectation",
                             [
                                 (UserAccessUsingTest.UNUSED_USERNAME, StatusCodes.INVALID_USERNAME),
                                 # test invalid username
                                 (UserAccessUsingTest.USERNAME_3, None)  # test valid username
                             ])
    def test_validate_username(self, app_context, validator, username, expectation):
        r = validator.validate_username(username)
        if isinstance(r, Response):
            assert r.status_code == expectation
        else:
            assert r == expectation

    @pytest.mark.parametrize("username, password_hash, expectation",
                             [
                                 (UserAccessUsingTest.UNUSED_USERNAME, UserAccessUsingTest.PASSWORD_1_HASH,
                                  StatusCodes.INVALID_USERNAME),  # test invalid username
                                 (UserAccessUsingTest.USERNAME_1, UserAccessUsingTest.PASSWORD_2_HASH,
                                  StatusCodes.INVALID_PASSWORD),  # test wrong password
                                 (UserAccessUsingTest.USERNAME_3, UserAccessUsingTest.PASSWORD_3_HASH, None)
                                 # test valid login
                             ])
    def test_validate_login(self, app_context, validator, username, password_hash, expectation):
        r = validator.validate_login(username, password_hash)
        if isinstance(r, Response):
            assert r.status_code == expectation
        else:
            assert r == expectation


class TestTaskGroupValidator(FlaskTest, TaskGroupAccessUsingTest):

    @pytest.fixture
    def validator(self, task_group_access):
        return TaskGroupValidator(task_group_access)

    @pytest.mark.parametrize("group_id, expectation", [
        (str(TaskGroupAccessUsingTest.GROUP_1), TaskGroupAccessUsingTest.GROUP_1),
        (str(TaskGroupAccessUsingTest.UNUSED_ID), StatusCodes.INVALID_IDENTIFIER),
        ("sfkl3:", StatusCodes.INVALID_IDENTIFIER),
        (str(TaskGroupAccessUsingTest.GROUP_2), TaskGroupAccessUsingTest.GROUP_2)])
    def test_validate_group_id(self, app_context, validator, group_id, expectation):
        r = validator.validate_group_id(group_id)
        if isinstance(r, Response):
            assert r.status_code == expectation
        else:
            assert r == expectation


class TestTaskValidator(FlaskTest, TaskAccessUsingTest):

    @pytest.fixture
    def validator(self, task_access):
        return TaskValidator(task_access)

    @pytest.mark.parametrize("task_id, expectation", [
        (str(TaskAccessUsingTest.TASK_3), TaskAccessUsingTest.TASK_3),
        (str(TaskAccessUsingTest.UNUSED_ID), StatusCodes.INVALID_IDENTIFIER),
        ("NOT AN INTEGER_", StatusCodes.INVALID_IDENTIFIER),
        (str(TaskAccessUsingTest.TASK_1), TaskAccessUsingTest.TASK_1)])
    def test_validate_group_id(self, app_context, validator, task_id, expectation):
        r = validator.validate_task_id(task_id)
        if isinstance(r, Response):
            assert r.status_code == expectation
        else:
            assert r == expectation
