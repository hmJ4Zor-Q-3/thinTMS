from unittest.mock import Mock

import pytest
import requests

from src.routes.auth_routes import UserApi
from src.test.util import test_util

AUTH_EXPECTED_RESULT = "a"
LOGOUT_EXPECTED_RESULT = "b"
REGISTER_EXPECTED_RESULT = "c"


@pytest.fixture
def app_process(request):
    """
    Creates a flask server running on another thread with mocked implementations.
    Returns:

    """
    m = Mock()
    m.auth.return_value = AUTH_EXPECTED_RESULT
    m.logout.return_value = LOGOUT_EXPECTED_RESULT
    m.register.return_value = REGISTER_EXPECTED_RESULT

    p = test_util.start_app_process_with_endpoints(UserApi(m))
    request.addfinalizer(lambda: test_util.close_app_process(p))
    return p


@pytest.fixture
def placeholder_credentials():
    return {UserApi.USERNAME_KEY: "u", UserApi.PASSWORD_KEY: "p"}


@pytest.fixture
def placeholder_session():
    return {UserApi.USERNAME_KEY: "u", UserApi.AUTH_TOKEN_KEY: "a"}


def test_auth_endpoint_1(app_process, placeholder_credentials):
    response = requests.get(f"http://{test_util.HOST}:{test_util.PORT}{UserApi.AUTH_ENDPOINT_PATH}",
                            params=placeholder_credentials)
    assert response.text == AUTH_EXPECTED_RESULT


def test_logout_endpoint_1(app_process, placeholder_session):
    response = requests.get(f"http://{test_util.HOST}:{test_util.PORT}{UserApi.LOGOUT_ENDPOINT_PATH}",
                            params=placeholder_session)
    assert response.text == LOGOUT_EXPECTED_RESULT


def test_register_endpoint_1(app_process, placeholder_credentials):
    response = requests.get(f"http://{test_util.HOST}:{test_util.PORT}{UserApi.REGISTER_ENDPOINT_PATH}",
                            params=placeholder_credentials)
    assert response.text == REGISTER_EXPECTED_RESULT
