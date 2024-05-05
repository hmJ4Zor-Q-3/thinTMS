import random
import string

import pytest
import requests

from src.database.task_group_database_manager import TaskGroupDatabaseManager
from src.routes.auth_routes import UserApi
from src.routes.status_codes import StatusCodes
from src.routes.task_routes import TaskApi
from src.test.server.tms_server_test import TMSServerTest


class TestTMSServerTaskGroupApi(TMSServerTest):

    @pytest.fixture
    def name(self):
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation,
                                      k=random.randint(0, TaskGroupDatabaseManager.NAME_LENGTH)))

    @pytest.fixture
    def long_name(self):
        too_long = TaskGroupDatabaseManager.NAME_LENGTH + 1
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation,
                                      k=random.randint(too_long, too_long)))

    def test_add_task_group_unused_user(self, tms_server):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: "fdmeo3L",
                                         UserApi.AUTH_TOKEN_KEY: "FFAAbb3c78",
                                         TaskApi.GROUP_NAME_KEY: "name"})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    def test_add_task_group_wrong_token(self, tms_server_with_users):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: self.mutate_token(tms_server_with_users[0].auth_token),
                                         TaskApi.GROUP_NAME_KEY: ")-02!DoWork-02}{"})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("auth_token", [
        "f8ad4ec6d72",  # test odd hex
        "",  # test empty string
        "sfk3",   # test even non-hex chars
        "sfkd3"  # test odd non-hex chars
    ])
    def test_add_task_group_unreadable_token(self, tms_server_with_users, auth_token):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: auth_token,
                                         TaskApi.GROUP_NAME_KEY: ")-02!DoWork-02}{"})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    def test_add_task_group_too_long_name(self, tms_server_with_users, long_name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: long_name})
        assert response.status_code == StatusCodes.BAD_REQUEST

    def test_add_task_group_success(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        assert isinstance(response.json()[TaskApi.GROUP_ID_KEY], int)

    def test_get_task_group_unused_user(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: TMSServerTest.UNUSED_USERNAME,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                        TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    def test_get_task_group_wrong_token(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: self.mutate_token(tms_server_with_users[0]),
                                        TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("auth_token", [
        "f8ad4ec6d72",  # test odd hex
        "",  # test empty string
        "sfk3",   # test even non-hex chars
        "sfkd3"  # test odd non-hex chars
    ])
    def test_get_task_group_unreadable_token(self, tms_server_with_users, name, auth_token):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: auth_token,
                                        TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    def test_get_task_group_not_authorized(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        iden = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[1].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[1].auth_token,
                                        TaskApi.GROUP_ID_KEY: iden})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("g_id", [
        132,  # test integral id
        1.1,  # test float id
        "d",  # test a non numeric id
    ])
    def test_get_task_group_invalid_key(self, tms_server_with_users, g_id):
        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                        TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_get_task_group_success(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                        TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.SUCCESS
        assert response.json()[TaskApi.GROUP_NAME_KEY] == name

    def test_update_task_group_unused_user(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: TMSServerTest.UNUSED_USERNAME,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_ID_KEY: g_id,
                                         TaskApi.GROUP_NAME_KEY: "probs not the current name."})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    def test_update_task_group_wrong_token(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: self.mutate_token(tms_server_with_users[0].auth_token),
                                         TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("auth_token", [
        "f8ad4ec6d72",  # test odd hex
        "",  # test empty string
        "sfk3",   # test even non-hex chars
        "sfkd3"  # test odd non-hex chars
    ])
    def test_update_task_group_unreadable_token(self, tms_server_with_users, name, auth_token):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: auth_token,
                                           TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    def test_update_task_group_not_authorized(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        iden = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[1].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[1].auth_token,
                                         TaskApi.GROUP_ID_KEY: iden})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("g_id", [
        132,  # test integral id
        1.1,  # test float id
        "d",  # test a non numeric id
    ])
    def test_update_task_group_invalid_key(self, tms_server_with_users, g_id):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_ID_KEY: g_id,
                                         TaskApi.GROUP_NAME_KEY: ""})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_update_task_group_excluded_name_success(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                        TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.SUCCESS
        assert (TaskApi.GROUP_NAME_KEY not in response.json()
                or response.json()[TaskApi.GROUP_NAME_KEY] == "")

    @pytest.mark.parametrize("new_name", [
        "",  # test empty name
        "3ko"
    ])
    def test_update_task_group_success(self, tms_server_with_users, name, new_name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_ID_KEY: g_id,
                                         TaskApi.GROUP_NAME_KEY: new_name})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                        TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.SUCCESS
        assert response.json()[TaskApi.GROUP_NAME_KEY] == new_name

    def test_delete_task_group_unused_user(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.delete(TMSServerTest.DELETE_TASK_GROUP_URL,
                                   params={UserApi.USERNAME_KEY: TMSServerTest.UNUSED_USERNAME,
                                           UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                           TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    def test_delete_task_group_wrong_token(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.delete(TMSServerTest.DELETE_TASK_GROUP_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: self.mutate_token(tms_server_with_users[0].auth_token),
                                           TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("auth_token", [
        "f8ad4ec6d72",  # test odd hex
        "",  # test empty string
        "sfk3",   # test even non-hex chars
        "sfkd3"  # test odd non-hex chars
    ])
    def test_delete_task_group_unreadable_token(self, tms_server_with_users, name, auth_token):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.delete(TMSServerTest.DELETE_TASK_GROUP_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: auth_token,
                                           TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    def test_delete_task_group_not_authorized(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        iden = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.delete(TMSServerTest.DELETE_TASK_GROUP_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_users[1].username,
                                           UserApi.AUTH_TOKEN_KEY: tms_server_with_users[1].auth_token,
                                           TaskApi.GROUP_ID_KEY: iden})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("g_id", [
        132,  # test integral id
        1.1,  # test float id
        "d",  # test a non numeric id
    ])
    def test_delete_task_group_invalid_key(self, tms_server_with_users, g_id):
        response = requests.delete(TMSServerTest.DELETE_TASK_GROUP_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                           TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_delete_task_group_success(self, tms_server_with_users, name):
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name})
        assert response.status_code == StatusCodes.SUCCESS
        g_id = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.delete(TMSServerTest.DELETE_TASK_GROUP_URL,
                                   params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                           UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                           TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TMSServerTest.GET_TASK_GROUP_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                        TaskApi.GROUP_ID_KEY: g_id})
        assert response.status_code == StatusCodes.INVALID_IDENTIFIER

    def test_get_task_groups_unused_user(self, tms_server_with_users):
        response = requests.get(TMSServerTest.GET_TASK_GROUPS_URL,
                                params={UserApi.USERNAME_KEY: TMSServerTest.UNUSED_USERNAME,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    def test_get_task_groups_wrong_token(self, tms_server_with_users, name):
        response = requests.get(TMSServerTest.GET_TASK_GROUPS_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: self.mutate_token(tms_server_with_users[0].auth_token)})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("auth_token", [
        "f8ad4ec6d72",  # test odd hex
        "",  # test empty string
        "sfk3",   # test even non-hex chars
        "sfkd3"  # test odd non-hex chars
    ])
    def test_get_task_groups_unreadable_token(self, tms_server_with_users, name, auth_token):
        response = requests.get(TMSServerTest.GET_TASK_GROUPS_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: auth_token})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    def test_get_task_groups_success(self, tms_server_with_users):
        name_1 = "one"
        name_2 = ""
        name_3 = "three"
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name_1})
        assert response.status_code == StatusCodes.SUCCESS
        g_id_1 = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[1].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[1].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name_2})
        assert response.status_code == StatusCodes.SUCCESS
        g_id_2 = response.json()[TaskApi.GROUP_ID_KEY]

        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                         UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token,
                                         TaskApi.GROUP_NAME_KEY: name_3})
        assert response.status_code == StatusCodes.SUCCESS
        g_id_3 = response.json()[TaskApi.GROUP_ID_KEY]

        u_0_g = [(g_id_1, name_1), (g_id_3, name_3)]
        u_1_g = [(g_id_2, name_2)]

        response = requests.get(TMSServerTest.GET_TASK_GROUPS_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[0].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[0].auth_token})
        assert response.status_code == StatusCodes.SUCCESS
        assert len(response.json()) == len(u_0_g)
        for i in range(0, len(u_0_g)):
            assert response.json()[i][TaskApi.GROUP_ID_KEY] == u_0_g[i][0]
            assert (TaskApi.GROUP_NAME_KEY not in response.json()[i]
                    or response.json()[i][TaskApi.GROUP_NAME_KEY] == u_0_g[i][1])

        response = requests.get(TMSServerTest.GET_TASK_GROUPS_URL,
                                params={UserApi.USERNAME_KEY: tms_server_with_users[1].username,
                                        UserApi.AUTH_TOKEN_KEY: tms_server_with_users[1].auth_token})
        assert response.status_code == StatusCodes.SUCCESS
        assert len(response.json()) == len(u_1_g)
        for i in range(0, len(u_1_g)):
            assert response.json()[i][TaskApi.GROUP_ID_KEY] == u_1_g[i][0]
            assert (TaskApi.GROUP_NAME_KEY not in response.json()[i]
                    or response.json()[i][TaskApi.GROUP_NAME_KEY] == u_1_g[i][1])

    # TODO, future, test groups associated with a user are delete when the user is deleted, not available currently.
