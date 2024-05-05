from collections import namedtuple

import pytest
import requests
from werkzeug.serving import make_server

from src.data.task_group import TaskGroup
from src.data.unidentified_task_group import UnIDTaskGroup
from src.routes.auth_routes import UserApi
from src.routes.task_routes import TaskApi
from src.server.server_thread import ServerThread
from src.server.tms_server import TMSServer
from src.test.util import test_util
from src.test.database.util.database_test_util import DatabaseTestUtil
from src.test.util.data.group_collection import GroupCollection
from src.test.util.data.user import User


class TMSServerTest(DatabaseTestUtil):
    PROTOCOL = "http"
    HOST = test_util.HOST
    PORT = test_util.PORT

    REGISTER_URL = f"{PROTOCOL}://{HOST}:{PORT}{UserApi.REGISTER_ENDPOINT_PATH}"
    LOGOUT_URL = f"{PROTOCOL}://{HOST}:{PORT}{UserApi.LOGOUT_ENDPOINT_PATH}"
    AUTH_URL = f"{PROTOCOL}://{HOST}:{PORT}{UserApi.AUTH_ENDPOINT_PATH}"

    GET_TASK_GROUPS_URL = f"{PROTOCOL}://{HOST}:{PORT}{TaskApi.TASK_GROUPS_ENDPOINT_PATH}"

    DELETE_TASK_GROUP_URL = f"{PROTOCOL}://{HOST}:{PORT}{TaskApi.TASK_GROUP_ENDPOINT_PATH}"
    GET_TASK_GROUP_URL = f"{PROTOCOL}://{HOST}:{PORT}{TaskApi.TASK_GROUP_ENDPOINT_PATH}"
    POST_TASK_GROUP_URL = f"{PROTOCOL}://{HOST}:{PORT}{TaskApi.TASK_GROUP_ENDPOINT_PATH}"

    DELETE_TASK_URL = f"{PROTOCOL}://{HOST}:{PORT}{TaskApi.TASK_ENDPOINT_PATH}"
    GET_TASK_URL = f"{PROTOCOL}://{HOST}:{PORT}{TaskApi.TASK_ENDPOINT_PATH}"
    POST_TASK_URL = f"{PROTOCOL}://{HOST}:{PORT}{TaskApi.TASK_ENDPOINT_PATH}"

    USER_1 = User("aNamed_3-4_", "Secure234_l4!", None)
    USER_2 = User("lowntuc82ld0#$Jf0r$", "Secure234_l4!", None)
    UNUSED_USERNAME = "3ld0LA0zuerhgvu9c"

    TASK_GROUP_1 = UnIDTaskGroup(USER_1.username, "title")
    TASK_GROUP_2 = UnIDTaskGroup(USER_1.username, "")
    TASK_GROUP_3 = UnIDTaskGroup(USER_2.username, "456789ijnbgt5")

    @pytest.fixture
    def tms_server(self, test_path):
        a = TMSServer(test_path).get_app()
        p = ServerThread(make_server(TMSServerTest.HOST, TMSServerTest.PORT, a))
        p.start()
        yield a
        p.kill()
        p.join()

    @pytest.fixture()
    def tms_server_with_users(self, tms_server) -> list[User]:
        return [self.register_user(TMSServerTest.USER_1.username, TMSServerTest.USER_1.password),
                self.register_user(TMSServerTest.USER_2.username, TMSServerTest.USER_2.password)]

    @pytest.fixture
    def tms_server_with_groups(self, tms_server_with_users):
        groups = [self.register_group(TMSServerTest.TASK_GROUP_1, tms_server_with_users),
                  self.register_group(TMSServerTest.TASK_GROUP_2, tms_server_with_users),
                  self.register_group(TMSServerTest.TASK_GROUP_3, tms_server_with_users)]
        return GroupCollection(tms_server_with_users, groups)

    def register_user(self, username: str, password: str) -> User:
        response = requests.get(TMSServerTest.REGISTER_URL,
                                params={UserApi.USERNAME_KEY: username,
                                        UserApi.PASSWORD_KEY: password})
        return User(username, password, response.json()[UserApi.AUTH_TOKEN_KEY][2:-1:])

    def register_group(self, group: UnIDTaskGroup, users: list[User]) -> TaskGroup:
        user = [x for x in users if x.username == group.username][0]
        response = requests.post(TMSServerTest.POST_TASK_GROUP_URL,
                                 params={UserApi.USERNAME_KEY: user.username,
                                         UserApi.AUTH_TOKEN_KEY: user.auth_token,
                                         TaskApi.GROUP_NAME_KEY: group.name})
        return TaskGroup.of(group, response.json()[TaskApi.GROUP_ID_KEY])

    def mutate_token(self, token: str):
        """
        Returns a token that's different from the one provided.
        Args:
            token:

        Returns:

        """
        t1 = "24cdf0346a0101d3e5b654526ee8977cdd1c206ae2b0b5da9aabeb3ff22d3a65"
        t2 = "3c02e992d001e64de2876f98eb07906429aa8756d8a2171c9f392b6bf501cbb3"
        return t2 if t1 == token else t1
