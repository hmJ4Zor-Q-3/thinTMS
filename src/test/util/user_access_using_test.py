import binascii
from unittest.mock import Mock

import pytest

from src.security.security import TMSSecurityStandard


class UserAccessUsingTest:
    SS = TMSSecurityStandard()

    USERNAME_1 = "userName"
    PASSWORD_1 = "Usme #0dk 0-L:"
    PASSWORD_1_HASH = SS.hash(PASSWORD_1)
    TOKEN_1 = binascii.unhexlify("21782ad56357d2d7f7cbc605f8b6e4d032f0db5ef0dea25ad73453241ff3c51a")

    USERNAME_2 = "Loei2Kpd84m"
    PASSWORD_2 = "0Pk3d_k3l-;feTs"
    PASSWORD_2_HASH = SS.hash(PASSWORD_2)
    TOKEN_2 = binascii.unhexlify("3087338e2d4d02f33d6564c1805c84d6885c973d277cae7e07eaf6fb6792befe")

    USERNAME_3 = "somebody"
    PASSWORD_3 = ":-O3ld_3k!~|dlL"
    PASSWORD_3_HASH = SS.hash(PASSWORD_3)
    TOKEN_3 = binascii.unhexlify("9bc4eb072012bdeff936c3a7b1eee4190921a15000dbdc83b85855191ab86cde")

    UNUSED_USERNAME = "flowers"
    CURRENT_SESSIONS = [(USERNAME_1, TOKEN_1),
                        (USERNAME_2, TOKEN_2),
                        (USERNAME_3, TOKEN_3)]

    REGISTERED_USERS = [(USERNAME_1, PASSWORD_1_HASH),
                        (USERNAME_2, PASSWORD_2_HASH),
                        (USERNAME_3, PASSWORD_3_HASH)]

    LOGIN_RESULT_1 = SS.create_auth_token()
    LOGIN_RESULT_2 = SS.create_auth_token()
    LOGOUT_RESULT_1 = 2
    LOGOUT_RESULT_2 = 4
    REGISTER_RESULT_1 = SS.create_auth_token()
    REGISTER_RESULT_2 = SS.create_auth_token()
    SS = None  # allow garbage collection of the security standard

    @pytest.fixture
    def user_access(self):
        """
        Creates a mock of an IUserAccess implementation.
        Returns:

        """
        ua_mock = Mock()

        ua_mock.login = Mock(side_effect=[UserAccessUsingTest.LOGIN_RESULT_1, UserAccessUsingTest.LOGIN_RESULT_2])
        ua_mock.logout = Mock(side_effect=[UserAccessUsingTest.LOGOUT_RESULT_1, UserAccessUsingTest.LOGOUT_RESULT_2])
        ua_mock.register_user = Mock(side_effect=[UserAccessUsingTest.REGISTER_RESULT_1,
                                                  UserAccessUsingTest.REGISTER_RESULT_2])

        ua_mock.is_user_registered = lambda u: u in [t[0] for t in UserAccessUsingTest.CURRENT_SESSIONS]
        ua_mock.is_user_login = lambda u, ph: (u, ph) in UserAccessUsingTest.REGISTERED_USERS
        ua_mock.is_valid_session = lambda u, t: (u, t) in UserAccessUsingTest.CURRENT_SESSIONS
        return ua_mock
