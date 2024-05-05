import calendar
import datetime
import random
import string

import pytest
import requests

from src.database.task_database_manager import TaskDatabaseManager
from src.routes.auth_routes import UserApi
from src.routes.status_codes import StatusCodes
from src.routes.task_routes import TaskApi
from src.test.server.tms_server_test import TMSServerTest


class TestTMSServerTaskGroupApi(TMSServerTest):

    @pytest.fixture
    def title(self):
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation,
                                      k=random.randint(0, TaskDatabaseManager.TITLE_LENGTH)))

    @pytest.fixture
    def description(self):
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation,
                                      k=random.randint(0, 512)))

    @pytest.fixture
    def date(self):
        year = random.randint(0, 9999)
        month = random.randint(1, 12)
        day = random.randint(1, calendar.monthrange(year, month)[1])
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"

    @pytest.fixture
    def long_title(self):
        too_long = TaskDatabaseManager.TITLE_LENGTH + 1
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation,
                                      k=random.randint(too_long, too_long)))

    def test_add_task_unused_username(self, tms_server):
        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: "kfkfl4r",
                                         UserApi.AUTH_TOKEN_KEY: "9034adce9f",
                                         TaskApi.GROUP_ID_KEY: 0,
                                         TaskApi.TASK_TITLE_KEY: "",
                                         TaskApi.TASK_DESCRIPTION_KEY: ""})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    def test_add_task_wrong_token(self, tms_server_with_users):
        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: self.mutate_token(tms_server_with_users[0].auth_token),
                                         TaskApi.GROUP_ID_KEY: 0,
                                         TaskApi.TASK_TITLE_KEY: "",
                                         TaskApi.TASK_DESCRIPTION_KEY: ""})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("token", [
        "",  # empty
        "1",  # not a pair
        "g",  # not hex character
        "aa 8ff"  # invalid character part way through
    ])
    def test_add_task_unreadable_token(self, tms_server_with_users, token):
        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: token,
                                         TaskApi.GROUP_ID_KEY: 0,
                                         TaskApi.TASK_TITLE_KEY: "",
                                         TaskApi.TASK_DESCRIPTION_KEY: ""})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    def test_add_task_invalid_group_identifier(self, tms_server_with_users):
        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_ID_KEY: 0,
                                         TaskApi.TASK_TITLE_KEY: "",
                                         TaskApi.TASK_DESCRIPTION_KEY: ""})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_add_task_title_too_long(self, tms_server_with_groups, long_title):
        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                         TaskApi.GROUP_ID_KEY: tms_server_with_groups.groups[0].identifier,
                                         TaskApi.TASK_TITLE_KEY: long_title,
                                         TaskApi.TASK_DESCRIPTION_KEY: ""})
        assert response.status_code == StatusCodes.BAD_REQUEST

    @pytest.mark.parametrize("bad_date", [
        "",  # empty
        "567ikjht5",  # nonesense
        "220009042T01:01:01"  # kinda almost valid
    ])
    def test_add_task_date_unreadable(self, tms_server_with_groups, title, description, bad_date):
        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                         TaskApi.GROUP_ID_KEY: tms_server_with_groups.groups[0].identifier,
                                         TaskApi.TASK_TITLE_KEY: title,
                                         TaskApi.TASK_DESCRIPTION_KEY: description,
                                         TaskApi.TASK_DATE_KEY: bad_date})
        assert response.status_code == StatusCodes.MISFORMATTED_DATE

    @pytest.mark.parametrize("t, d, dd", [
        (None, None, None),  # with all excluded
        ("sndeo03_ + =2", None, None),  # only a title
        (None, "description of the task s.", None),  # only a description
        (None, None, "2167-09-13T12:03:34"),  # only a date
        ("", "None", None),  # title and description
        (None, "", "5873-01-11T14:00:01"),  # description and date
        ("Titular", None, "5873-01-11T14:00:01"),  # title and date
        ("3mohy50", "rtyujnbvfdrty ujhgfr 6yujgfr 567ujnbfrt yjnvfrtyh j", "0130-12-31T21:07:27"),  # all
    ])
    def test_add_task_success(self, tms_server_with_groups, t, d, dd):
        #  create json dict conditionally and paramaterize to test various field exemptions.
        data = self.conditionally_add(
            {UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
             UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
             TaskApi.GROUP_ID_KEY: tms_server_with_groups.groups[0].identifier}, t, d, dd)

        response = requests.post(TMSServerTest.POST_TASK_URL, params=data)
        assert response.status_code == StatusCodes.SUCCESS
        assert isinstance(response.json()[TaskApi.TASK_ID_KEY], int)

    def test_get_task_unused_user(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.get(TMSServerTest.GET_TASK_URL,
                                params={UserApi.USERNAME_KEY: TMSServerTest.UNUSED_USERNAME,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                        TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    def test_get_task_wrong_token(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.get(TMSServerTest.GET_TASK_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: self.mutate_token(tms_server_with_groups.users[0].auth_token),
                                        TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("auth_token", [
        "f8ad4ec6d72",  # test odd hex
        "",  # test empty string
        "sfk3",   # test even non-hex chars
        "sfkd3"  # test odd non-hex chars
    ])
    def test_get_task_unreadable_token(self, tms_server_with_groups, title, description, date, auth_token):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.get(TMSServerTest.GET_TASK_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: auth_token,
                                        TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    def test_get_task_not_authorized(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.get(TMSServerTest.GET_TASK_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_groups.users[1].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[1].auth_token,
                                        TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("t_id", [
        132,  # test integral id
        1.1,  # test float id
        "d",  # test a non numeric id
    ])
    def test_get_task_invalid_task_id(self, tms_server_with_users, t_id):
        response = requests.get(TMSServerTest.GET_TASK_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                        TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_get_task_success(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.get(TMSServerTest.GET_TASK_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                        TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.SUCCESS
        assert response.json()[TaskApi.TASK_TITLE_KEY] == title
        assert response.json()[TaskApi.TASK_DESCRIPTION_KEY] == description
        assert datetime.datetime.fromisoformat(response.json()[TaskApi.TASK_DATE_KEY]) == datetime.datetime.fromisoformat(date)

    def test_update_task_unused_user(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: TMSServerTest.UNUSED_USERNAME,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                         TaskApi.TASK_ID_KEY: t_id,
                                         TaskApi.TASK_TITLE_KEY: "probs not the current name."})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    def test_update_task_wrong_token(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: self.mutate_token(tms_server_with_groups.users[0].auth_token),
                                         TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("auth_token", [
        "f8ad4ec6d72",  # test odd hex
        "",  # test empty string
        "sfk3",   # test even non-hex chars
        "sfkd3"  # test odd non-hex chars
    ])
    def test_update_task_unreadable_token(self, tms_server_with_groups, title, description, date, auth_token):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: auth_token,
                                         TaskApi.TASK_ID_KEY:t_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    def test_update_task_not_authorized(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_groups.users[1].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[1].auth_token,
                                         TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("t_id", [
        132,  # test integral id
        1.1,  # test float id
        "d",  # test a non numeric id
    ])
    def test_update_task_invalid_task_id(self, tms_server_with_users, t_id):
        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.TASK_ID_KEY: t_id,
                                         TaskApi.TASK_TITLE_KEY: ""})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_update_task_title_too_long(self, tms_server_with_groups, title, description, date, long_title):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                         TaskApi.TASK_ID_KEY: t_id,
                                         TaskApi.TASK_TITLE_KEY: long_title})
        assert response.status_code == StatusCodes.BAD_REQUEST

    @pytest.mark.parametrize("bad_date", [
        "",  # empty
        "567ikjht5",  # nonesense
        "220009042T01:01:01"  # kinda almost valid
    ])
    def test_update_task_date_unreadable(self, tms_server_with_groups, title, description, date, bad_date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.post(TMSServerTest.POST_TASK_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                         TaskApi.TASK_ID_KEY: t_id,
                                         TaskApi.TASK_DATE_KEY: bad_date})
        assert response.status_code == StatusCodes.MISFORMATTED_DATE

    @pytest.mark.parametrize("t, d, dd", [
        (None, None, None),  # with all excluded
        ("sndeo03_ + =2", None, None),  # only a title
        (None, "description of the task s.", None),  # only a description
        (None, None, "2167-09-13T12:03:34"),  # only a date
        ("", "None", None),  # title and description
        (None, "", "5873-01-11T14:00:01"),  # description and date
        ("Titular", None, "5873-01-11T14:00:01"),  # title and date
        ("3mohy50", "rtyujnbvfdrty ujhgfr 6yujgfr 567ujnbfrt yjnvfrtyh j", "0130-12-31T21:07:27"),  # all
    ])
    def test_update_task_success(self, tms_server_with_groups, title, description, date, t, d, dd):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        data = self.conditionally_add({UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                       UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                       TaskApi.TASK_ID_KEY: t_id}, t, d, dd)
        response = requests.post(TMSServerTest.POST_TASK_URL, params=data)
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TMSServerTest.GET_TASK_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                        TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.SUCCESS
        assert (((TaskApi.TASK_TITLE_KEY not in response.json() or response.json()[TaskApi.TASK_TITLE_KEY] == "") and t is None)
                or (response.json()[TaskApi.TASK_TITLE_KEY] == t))

        assert (((TaskApi.TASK_DESCRIPTION_KEY not in response.json() or response.json()[TaskApi.TASK_DESCRIPTION_KEY] == "") and d is None)
                or (response.json()[TaskApi.TASK_DESCRIPTION_KEY] == d))

        assert (((TaskApi.TASK_DATE_KEY not in response.json() or response.json()[TaskApi.TASK_DATE_KEY] == "") and dd is None)
                or (datetime.datetime.fromisoformat(response.json()[TaskApi.TASK_DATE_KEY]) == datetime.datetime.fromisoformat(dd)))

    def test_delete_task_unused_user(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.delete(TMSServerTest.DELETE_TASK_URL,
                                   params={UserApi.USERNAME_KEY: TMSServerTest.UNUSED_USERNAME,
                                           UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                           TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    def test_delete_task_wrong_token(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.delete(TMSServerTest.DELETE_TASK_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: self.mutate_token(tms_server_with_groups.users[0].auth_token),
                                           TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("auth_token", [
        "f8ad4ec6d72",  # test odd hex
        "",  # test empty string
        "sfk3",   # test even non-hex chars
        "sfkd3"  # test odd non-hex chars
    ])
    def test_delete_task_unreadable_token(self, tms_server_with_groups, title, description, date, auth_token):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.delete(TMSServerTest.DELETE_TASK_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: auth_token,
                                           TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    def test_delete_task_not_authorized(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.delete(TMSServerTest.DELETE_TASK_GROUP_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_groups.users[1].username,
                                           UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[1].auth_token,
                                           TaskApi.GROUP_ID_KEY: t_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("t_id", [
        132,  # test integral id
        1.1,  # test float id
        "d",  # test a non numeric id
    ])
    def test_delete_task_invalid_key(self, tms_server_with_users, t_id):
        response = requests.delete(TMSServerTest.DELETE_TASK_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                           TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_delete_task_success(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.delete(TMSServerTest.DELETE_TASK_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                           TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TMSServerTest.GET_TASK_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                        TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_group_delete_deletes_tasks(self, tms_server_with_groups, title, description, date):
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.delete(TMSServerTest.DELETE_TASK_GROUP_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                           TaskApi.GROUP_ID_KEY: tms_server_with_groups.groups[0].identifier})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                        TaskApi.GROUP_ID_KEY: tms_server_with_groups.groups[0].identifier})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

        response = requests.get(TMSServerTest.GET_TASK_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                        TaskApi.TASK_ID_KEY: t_id})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_get_group_gets_tasks(self, tms_server_with_groups, title, description, date):
        # TODO, maybe add multiple, and exclusion tests.
        t_id = self.add_task(tms_server_with_groups.users[0].username,
                             tms_server_with_groups.users[0].auth_token,
                             tms_server_with_groups.groups[0].identifier,
                             title,
                             description,
                             date)

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_groups.users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_groups.users[0].auth_token,
                                        TaskApi.GROUP_ID_KEY: tms_server_with_groups.groups[0].identifier})
        assert response.status_code == StatusCodes.SUCCESS
        assert response.json()[TaskApi.GROUP_NAME_KEY] == tms_server_with_groups.groups[0].name

        assert len(response.json()["contents"]) == 1
        assert response.json()["contents"][0][TaskApi.TASK_ID_KEY] == t_id
        assert response.json()["contents"][0][TaskApi.TASK_TITLE_KEY] == title
        assert TaskApi.TASK_DESCRIPTION_KEY not in response.json()["contents"][0]
        assert (datetime.datetime.fromisoformat(response.json()["contents"][0][TaskApi.TASK_DATE_KEY])
                == datetime.datetime.fromisoformat(date))





    def add_task(self, username, auth_token, group_identifier, title, description, date) -> int:
        data = {UserApi.USERNAME_KEY: username,
                UserApi.AUTH_TOKEN_KEY: auth_token,
                TaskApi.GROUP_ID_KEY: group_identifier}
        data = self.conditionally_add(data, title, description, date)

        return requests.post(TMSServerTest.POST_TASK_URL, params=data).json()[TaskApi.TASK_ID_KEY]

    def conditionally_add(self, data: dict, title, description, date) -> dict:
        if title is not None:
            data[TaskApi.TASK_TITLE_KEY] = title

        if description is not None:
            data[TaskApi.TASK_DESCRIPTION_KEY] = description

        if date is not None:
            data[TaskApi.TASK_DATE_KEY] = date

        return data
