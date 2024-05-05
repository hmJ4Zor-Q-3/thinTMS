import pytest

from src.database.user_database_manager import UserDatabaseManager
from src.exceptions.exceptions import UsernameError, PasswordError, AuthTokenError
from src.test.database.util.user_database_test_util import UserDatabaseTestUtil


class TestUserDatabaseManager(UserDatabaseTestUtil):

    def test___init__(self, user_inst):
        with user_inst.connection():
            assert len(user_inst.cursor.execute(
                "SELECT name "
                "FROM sqlite_master "
                "WHERE type='table' AND name=?",
                (UserDatabaseManager.USER_TABLE_NAME,)).fetchall()) == 1

    @pytest.mark.parametrize("username, password_hash",
    [
        (UserDatabaseTestUtil.USERNAME_1, UserDatabaseTestUtil.PASSWORD_1_HASH),  # test valid login
        (UserDatabaseTestUtil.USERNAME_2, UserDatabaseTestUtil.PASSWORD_2_HASH),  # test valid login
    ])
    def test_login_success(self, populated_user_inst, username, password_hash):
        assert isinstance(populated_user_inst.login(username, password_hash), bytes)

    def test_login_user_error(self, populated_user_inst):
        with pytest.raises(UsernameError):
            populated_user_inst.login(TestUserDatabaseManager.UNUSED_USERNAME, TestUserDatabaseManager.PASSWORD_1_HASH)

    def test_login_password_error(self, populated_user_inst):
        with pytest.raises(PasswordError):
            populated_user_inst.login(TestUserDatabaseManager.USERNAME_1, TestUserDatabaseManager.PASSWORD_3_HASH)

    @pytest.mark.parametrize("username, auth_token",
    [
        (UserDatabaseTestUtil.USERNAME_1, UserDatabaseTestUtil.TOKEN_1),  # test valid session
        (UserDatabaseTestUtil.USERNAME_3, UserDatabaseTestUtil.TOKEN_3),  # test valid session
    ])
    def test_logout_success(self, populated_user_inst, username, auth_token):
        assert populated_user_inst.is_valid_session(username, auth_token)
        populated_user_inst.logout(username, auth_token)
        assert not populated_user_inst.is_valid_session(username, auth_token)

    def test_logout_username_error(self, populated_user_inst):
        with pytest.raises(UsernameError):
            populated_user_inst.logout(TestUserDatabaseManager.UNUSED_USERNAME, TestUserDatabaseManager.TOKEN_1)

    @pytest.mark.parametrize("username, auth_token",
                             [
                                 (UserDatabaseTestUtil.USERNAME_2, UserDatabaseTestUtil.TOKEN_1),  # test user without active session
                                 (UserDatabaseTestUtil.USERNAME_1, UserDatabaseTestUtil.TOKEN_3),  # test user with session but wrong token
                             ])
    def test_logout_token_error(self, populated_user_inst, username, auth_token):
        with pytest.raises(AuthTokenError):
            populated_user_inst.logout(username, auth_token)

    @pytest.mark.parametrize("username, password_hash",
                             [
                                 (UserDatabaseTestUtil.UNUSED_USERNAME, UserDatabaseTestUtil.PASSWORD_1_HASH)
                             ])
    def test_register_user(self, populated_user_inst, username, password_hash):
        token = populated_user_inst.register_user(username, password_hash)
        assert populated_user_inst.is_user_registered(username)
        assert populated_user_inst.is_valid_session(username, token)

    def test_register_user_username_error(self, populated_user_inst):
        with pytest.raises(UsernameError):
            populated_user_inst.register_user(TestUserDatabaseManager.USERNAME_1, TestUserDatabaseManager.PASSWORD_2_HASH)

    @pytest.mark.parametrize("username, expected_result",
    [
        (UserDatabaseTestUtil.UNUSED_USERNAME, False),  # test not registered
        (UserDatabaseTestUtil.USERNAME_1, True),  # test is registered
    ])
    def test_is_user_registered(self, populated_user_inst, username, expected_result):
        assert populated_user_inst.is_user_registered(username) == expected_result

    @pytest.mark.parametrize("username, password_hash, expected_result",
    [
        (UserDatabaseTestUtil.USERNAME_3, UserDatabaseTestUtil.PASSWORD_2_HASH, False),  # test mismatched login
        (UserDatabaseTestUtil.USERNAME_1, UserDatabaseTestUtil.PASSWORD_1_HASH, True)  # test valid login
    ])
    def test_is_user_login_1(self, populated_user_inst, username, password_hash, expected_result):
        assert populated_user_inst.is_user_login(username, password_hash) == expected_result

    def test_is_user_login_2(self, populated_user_inst):
        with pytest.raises(UsernameError):
            populated_user_inst.is_user_login(TestUserDatabaseManager.UNUSED_USERNAME,
                                              TestUserDatabaseManager.PASSWORD_2_HASH)

    @pytest.mark.parametrize("username, token, excepted_result",
    [
        (UserDatabaseTestUtil.USERNAME_3, UserDatabaseTestUtil.TOKEN_1, False),  # test wrong token
        (UserDatabaseTestUtil.USERNAME_2, UserDatabaseTestUtil.TOKEN_1, False),  # test doesn't have a token
        (UserDatabaseTestUtil.USERNAME_3, UserDatabaseTestUtil.TOKEN_3, True)  # test valid login
    ])
    def test_is_valid_session_1(self, populated_user_inst, username, token, excepted_result):
        assert populated_user_inst.is_valid_session(username, token) == excepted_result

    def test_is_valid_session_2(self, populated_user_inst):
        with pytest.raises(UsernameError):
            populated_user_inst.is_valid_session(TestUserDatabaseManager.UNUSED_USERNAME, TestUserDatabaseManager.TOKEN_1)
