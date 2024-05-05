import binascii

import pytest

from src.routes.auth_routes import UserApi
from src.routes.implementation.tms_user_implementation import TMSUserApiImpl
from src.routes.status_codes import StatusCodes
from src.security.security import TMSSecurityStandard
from src.test.util.test_util import FlaskTest
from src.test.util.user_access_using_test import UserAccessUsingTest


class TestTMSUserApiImpl(FlaskTest, UserAccessUsingTest):

    @pytest.fixture
    def impl(self, user_access):
        """
        Generates a TMSUserApiImpl.
        Args:
            user_access:

        Returns:

        """
        i = TMSUserApiImpl(user_access, TMSSecurityStandard())
        return i

    @pytest.mark.parametrize("username, password, expected_code, method_expectation",
                             [
                                 (UserAccessUsingTest.UNUSED_USERNAME, UserAccessUsingTest.PASSWORD_1,
                                  StatusCodes.INVALID_USERNAME, UserAccessUsingTest.LOGIN_RESULT_1),
                                 # not register username
                                 (UserAccessUsingTest.USERNAME_1, UserAccessUsingTest.PASSWORD_2,
                                  StatusCodes.INVALID_PASSWORD, UserAccessUsingTest.LOGIN_RESULT_1),
                                 # password doesn't match
                                 (UserAccessUsingTest.USERNAME_2, UserAccessUsingTest.PASSWORD_2, StatusCodes.SUCCESS,
                                  UserAccessUsingTest.LOGIN_RESULT_2)  # test valid call
                             ])
    def test_auth(self, app_context, impl, username, password, expected_code, method_expectation):
        r = impl.auth(username, password)
        assert r.status_code == expected_code
        assert impl._ua.login() == method_expectation

    def test_auth_format(self, app_context, impl):
        # test success format matches this: {"token": string}
        r = impl.auth(UserAccessUsingTest.USERNAME_1, UserAccessUsingTest.PASSWORD_1)
        assert r.is_json
        assert isinstance(r.json[UserApi.AUTH_TOKEN_KEY], str)

    @pytest.mark.parametrize("username, token, expected_code, method_expectation",
                             [
                                 (UserAccessUsingTest.UNUSED_USERNAME, binascii.hexlify(UserAccessUsingTest.TOKEN_3),
                                  StatusCodes.INVALID_USERNAME, UserAccessUsingTest.LOGOUT_RESULT_1),
                                 # test nonexistent username
                                 (UserAccessUsingTest.USERNAME_3, "0.3l", StatusCodes.UNAUTHORIZED,
                                  UserAccessUsingTest.LOGOUT_RESULT_1),  # test token unparseable
                                 (UserAccessUsingTest.USERNAME_2, binascii.hexlify(UserAccessUsingTest.TOKEN_3),
                                  StatusCodes.UNAUTHORIZED, UserAccessUsingTest.LOGOUT_RESULT_1),  # test token mismatch
                                 (UserAccessUsingTest.USERNAME_1, binascii.hexlify(UserAccessUsingTest.TOKEN_1),
                                  StatusCodes.SUCCESS, UserAccessUsingTest.LOGOUT_RESULT_2)  # test valid request
                             ])
    def test_logout(self, app_context, impl, username, token, expected_code, method_expectation):
        r = impl.logout(username, token)
        assert r.status_code == expected_code
        assert impl._ua.logout() == method_expectation

    @pytest.mark.parametrize("username, password, expected_code, method_expectation",
                             [
                                 (UserAccessUsingTest.USERNAME_1, UserAccessUsingTest.PASSWORD_1,
                                  StatusCodes.INVALID_USERNAME, UserAccessUsingTest.REGISTER_RESULT_1),
                                 # already registered username
                                 (UserAccessUsingTest.UNUSED_USERNAME, "a", StatusCodes.INVALID_PASSWORD,
                                  UserAccessUsingTest.REGISTER_RESULT_1),  # (various) weak password
                                 (UserAccessUsingTest.UNUSED_USERNAME, "nocaps_102l2", StatusCodes.INVALID_PASSWORD,
                                  UserAccessUsingTest.REGISTER_RESULT_1),  # (various) weak password
                                 (UserAccessUsingTest.UNUSED_USERNAME, "Short8_", StatusCodes.INVALID_PASSWORD,
                                  UserAccessUsingTest.REGISTER_RESULT_1),  # (various) weak password
                                 (UserAccessUsingTest.UNUSED_USERNAME, UserAccessUsingTest.PASSWORD_2,
                                  StatusCodes.SUCCESS, UserAccessUsingTest.REGISTER_RESULT_2)  # test valid call
                             ])
    def test_register(self, app_context, impl, username, password, expected_code, method_expectation):
        r = impl.register(username, password)
        assert r.status_code == expected_code
        assert impl._ua.register_user() == method_expectation

    def test_register_format(self, app_context, impl):
        # test success format matches this: {"token": string}
        r = impl.register(UserAccessUsingTest.UNUSED_USERNAME, UserAccessUsingTest.PASSWORD_1)
        assert r.is_json
        assert isinstance(r.json[UserApi.AUTH_TOKEN_KEY], str)
