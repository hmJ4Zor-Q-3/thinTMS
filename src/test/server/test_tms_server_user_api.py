import random
import re
import string

import pytest
import requests

from src.database.user_database_manager import UserDatabaseManager
from src.routes.auth_routes import UserApi
from src.routes.status_codes import StatusCodes
from src.test.server.tms_server_test import TMSServerTest


class TestTMSServerUserApi(TMSServerTest):

    @pytest.fixture
    def long_username(self):
        too_long = UserDatabaseManager.USERNAME_LENGTH + 1
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation,
                                      k=random.randint(too_long, too_long)))

    @pytest.mark.parametrize("username, password",
                             [("a", "2Lo_op32xkl-;")])
    def test_register_success(self, tms_server, username, password):
        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.SUCCESS

    @pytest.mark.parametrize("password",
                             ["_2xoLk89-o3pl;"])
    def test_register_username_too_long(self, tms_server, long_username, password):
        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: long_username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.BAD_REQUEST

    @pytest.mark.parametrize("username, password",
                             [("aVerbose name", "p9Losdlob_ol-xk2;")])
    def test_register_used_username(self, tms_server, username, password):
        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    @pytest.mark.parametrize("username, password",
                             [("aVerbose name", "ceuy3k-0*3%,"),  # test no capital
                              ("34f", "PASSWORD-LONG1"),  # test no lowercase
                              ("name", "not_a_number"),  # test no number
                              ("name2", "ContainsNoSymbols2"),  # test no symbol
                              ("alsoAName", "short_3lo")  # test too short
                              ])
    def test_register_user_weak_password(self, tms_server, username, password):
        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.INVALID_PASSWORD

    @pytest.mark.parametrize("username, password",
                             [("aVerbose name", "p9Losdlob_ol-xk2;")])
    def test_logout_success(self, tms_server, username, password):
        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.SUCCESS
        token = response.json()[UserApi.AUTH_TOKEN_KEY][2:-1:]  # trims b'...' leaving the ...

        response = requests.get(TestTMSServerUserApi.LOGOUT_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.AUTH_TOKEN_KEY: token})
        assert response.status_code == StatusCodes.SUCCESS

    @pytest.mark.parametrize("username, token",
                             [("not_registered", "affa")])
    def test_logout_unused_username(self, tms_server, username, token):
        response = requests.get(TestTMSServerUserApi.LOGOUT_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.AUTH_TOKEN_KEY: token})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    @pytest.mark.parametrize("username, token",
                             [("r", "afggfa")])
    def test_logout_unreadable_token(self, tms_server, username, token):
        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: "apasSwoRd0_03"})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TestTMSServerUserApi.LOGOUT_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.AUTH_TOKEN_KEY: token})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("username, token",
                             [("fffeg", "9029def8")])
    def test_logout_wrong_token(self, tms_server, username, token):
        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: "aRd0sSwa_fpo03"})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TestTMSServerUserApi.LOGOUT_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.AUTH_TOKEN_KEY: token})
        assert response.status_code == StatusCodes.UNAUTHORIZED

    @pytest.mark.parametrize("username, password",
                             [("llll", "cV&^BV&^B8n98uj")])
    def test_authorize_success(self, tms_server, username, password):
        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TestTMSServerUserApi.AUTH_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.SUCCESS
        token = response.json()[UserApi.AUTH_TOKEN_KEY][2:-1:]  # trims b'...' leaving the ...
        assert (len(token) % 2) == 0
        assert re.match("^[0-9a-f]+$", token) is not None

    @pytest.mark.parametrize("username, password",
                             [("llll", "cV&^BV&^B8n98uj")])
    def test_authorize_unused_username(self, tms_server, username, password):
        response = requests.get(TestTMSServerUserApi.AUTH_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.INVALID_USERNAME

    @pytest.mark.parametrize("username, password, wrong_password",
                             [("User3.0", "kg5G%gT$3g$3btgR", "kg5G%gT$3g$3btgr")])
    def test_authorize_wrong_password(self, tms_server, username, password, wrong_password):
        response = requests.get(TestTMSServerUserApi.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: password})
        assert response.status_code == StatusCodes.SUCCESS

        response = requests.get(TestTMSServerUserApi.AUTH_URL,
                                params={UserApi.USERNAME_KEY: username, UserApi.PASSWORD_KEY: wrong_password})
        assert response.status_code == StatusCodes.INVALID_PASSWORD

    # test data persistence
