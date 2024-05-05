from unittest.mock import Mock

import pytest
import requests

from src.routes.auth_routes import UserApi
from src.routes.status_codes import StatusCodes
from src.routes.task_routes import TaskApi
from src.test.util import test_util

GTGS_EXPECTED_RESULT = "a"
DTG_EXPECTED_RESULT = "b"
GTG_EXPECTED_RESULT = "c"
PTG_EXPECTED_RESULT = "d"
DT_EXPECTED_RESULT = "e"
GT_EXPECTED_RESULT = "f"
PT_EXPECTED_RESULT = "g"


@pytest.fixture
def app_process(request):
    """
    Creates a flask server running on another thread with mocked implementations.
    Returns:

    """
    m = Mock()
    m.get_task_groups.return_value = GTGS_EXPECTED_RESULT
    m.delete_task_group.return_value = DTG_EXPECTED_RESULT
    m.get_task_group.return_value = GTG_EXPECTED_RESULT
    m.post_task_group.return_value = PTG_EXPECTED_RESULT
    m.delete_task.return_value = DT_EXPECTED_RESULT
    m.get_task.return_value = GT_EXPECTED_RESULT
    m.post_task.return_value = PT_EXPECTED_RESULT

    p = test_util.start_app_process_with_endpoints(TaskApi(m))
    request.addfinalizer(lambda: test_util.close_app_process(p))
    return p


@pytest.fixture
def session():
    return {UserApi.USERNAME_KEY: "u", UserApi.AUTH_TOKEN_KEY: "a"}


@pytest.fixture
def authorized_group(session):
    session[TaskApi.GROUP_ID_KEY] = "1"
    return session


@pytest.fixture
def authorized_task(session):
    session[TaskApi.TASK_ID_KEY] = "1"
    return session


def test_get_task_groups_endpoint_1(app_process, session):
    response = requests.get(f"http://{test_util.HOST}:{test_util.PORT}{TaskApi.TASK_GROUPS_ENDPOINT_PATH}",
                            params=session)
    assert response.text == GTGS_EXPECTED_RESULT


def test_delete_task_group_endpoint_1(app_process, authorized_group):
    response = requests.delete(f"http://{test_util.HOST}:{test_util.PORT}{TaskApi.TASK_GROUP_ENDPOINT_PATH}",
                               params=authorized_group)
    assert response.text == DTG_EXPECTED_RESULT


def test_get_task_group_endpoint_1(app_process, authorized_group):
    response = requests.get(f"http://{test_util.HOST}:{test_util.PORT}{TaskApi.TASK_GROUP_ENDPOINT_PATH}",
                            params=authorized_group)
    assert response.text == GTG_EXPECTED_RESULT


def test_post_task_group_endpoint_1(app_process, session):
    response = requests.post(f"http://{test_util.HOST}:{test_util.PORT}{TaskApi.TASK_GROUP_ENDPOINT_PATH}",
                             params=session)
    assert response.text == PTG_EXPECTED_RESULT


def test_delete_task_endpoint_1(app_process, authorized_task):
    response = requests.delete(f"http://{test_util.HOST}:{test_util.PORT}{TaskApi.TASK_ENDPOINT_PATH}",
                               params=authorized_task)
    assert response.text == DT_EXPECTED_RESULT


def test_get_task_endpoint_1(app_process, authorized_task):
    response = requests.get(f"http://{test_util.HOST}:{test_util.PORT}{TaskApi.TASK_ENDPOINT_PATH}",
                            params=authorized_task)
    assert response.text == GT_EXPECTED_RESULT


def test_post_task_endpoint_1(app_process, session):
    response = requests.post(f"http://{test_util.HOST}:{test_util.PORT}{TaskApi.TASK_ENDPOINT_PATH}",
                             params=session)
    assert response.status_code == StatusCodes.SUCCESS  # technically a success, neither group not task id're always required, just one or the other


def test_post_task_endpoint_2(app_process, authorized_group):
    response = requests.post(f"http://{test_util.HOST}:{test_util.PORT}{TaskApi.TASK_ENDPOINT_PATH}",
                             params=authorized_group)
    assert response.text == PT_EXPECTED_RESULT
