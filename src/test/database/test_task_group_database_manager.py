import pytest

from src.data.task_group import TaskGroup
from src.data.unidentified_task_group import UnIDTaskGroup
from src.database.task_group_database_manager import TaskGroupDatabaseManager
from src.exceptions.exceptions import UsernameError
from src.test.database.util.task_group_database_test_util import TaskGroupDatabaseTestUtil
from src.test.database.util.user_database_test_util import UserDatabaseTestUtil


class TestTaskGroupDatabaseManager(TaskGroupDatabaseTestUtil):

    def test___init__(self, task_group_inst):
        with task_group_inst.connection():
            assert len(task_group_inst.cursor.execute(
                "SELECT name "
                "FROM sqlite_master "
                "WHERE type='table' AND name=?",
                (TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME,)).fetchall()) == 1

    @pytest.mark.parametrize("task_group",
    [
        UnIDTaskGroup(UserDatabaseTestUtil.USERNAME_1, ""),  # test add with a name that's empty
        UnIDTaskGroup(UserDatabaseTestUtil.USERNAME_1, "9032_0000_0000_0000_0000_0000_"),  # test add with longer name
        UnIDTaskGroup(UserDatabaseTestUtil.USERNAME_3, "__o--")  # test adding with longer name, and different account
    ])
    def test_add_task_group(self, task_group_inst, task_group: UnIDTaskGroup):
        r = task_group_inst.add_task_group(task_group)
        assert isinstance(r, TaskGroup)
        assert task_group_inst.is_group_registered(r.identifier)

    def test_add_task_group_unused_username(self, task_group_inst):
        with pytest.raises(UsernameError):
            task_group_inst.add_task_group(UnIDTaskGroup(UserDatabaseTestUtil.UNUSED_USERNAME, "groupN"))

    @pytest.mark.parametrize("group_id",
    [
        TaskGroupDatabaseTestUtil.TASK_GROUP_ID_1
    ])
    def test_delete_task_group(self, populated_task_group_inst, group_id: int):
        assert populated_task_group_inst.is_group_registered(group_id)
        populated_task_group_inst.delete_task_group(group_id)
        assert not populated_task_group_inst.is_group_registered(group_id)

    def test_delete_task_group_invalid_group_id(self, task_group_inst):
        with pytest.raises(KeyError):
            task_group_inst.delete_task_group(3)

    @pytest.mark.parametrize("group_id, expectation", [
        (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_1, TaskGroupDatabaseTestUtil.TASK_GROUP_1),
        (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2, TaskGroupDatabaseTestUtil.TASK_GROUP_2)
    ])
    def test_get_task_group(self, populated_task_group_inst, group_id: int, expectation: str):
        assert populated_task_group_inst.get_task_group(group_id) == expectation

    def test_get_task_group_invalid_group_id(self, task_group_inst):
        with pytest.raises(KeyError):
            task_group_inst.get_task_group(3)

    @pytest.mark.parametrize("username, expectation", [
        (UserDatabaseTestUtil.USERNAME_1, TaskGroupDatabaseTestUtil.USERNAME_1_GROUPS),
        (UserDatabaseTestUtil.USERNAME_2, TaskGroupDatabaseTestUtil.USERNAME_2_GROUPS),
        (UserDatabaseTestUtil.USERNAME_3, TaskGroupDatabaseTestUtil.USERNAME_3_GROUPS)
    ])
    def test_get_task_groups(self, populated_task_group_inst, username: str, expectation: list[TaskGroup]):
        assert populated_task_group_inst.get_task_groups(username) == expectation

    def test_get_task_groups_unused_username(self, task_group_inst):
        with pytest.raises(UsernameError):
            task_group_inst.get_task_groups(UserDatabaseTestUtil.UNUSED_USERNAME)

    @pytest.mark.parametrize("task_group", [
        TaskGroup("", "", TaskGroupDatabaseTestUtil.TASK_GROUP_ID_1),  # test empty name
        TaskGroup("", "NewName", TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2),  # test non empty name change
        TaskGroup("", TaskGroupDatabaseTestUtil.TASK_GROUP_NAME_3, TaskGroupDatabaseTestUtil.TASK_GROUP_ID_3)  # test change to same name
    ])
    def test_update_task_group(self, populated_task_group_inst, task_group: TaskGroup):
        populated_task_group_inst.update_task_group(task_group)

        assert populated_task_group_inst.get_task_group(task_group.identifier).name == task_group.name

    def test_update_task_group_invalid_group_id(self, task_group_inst):
        with pytest.raises(KeyError):
            task_group_inst.update_task_group(TaskGroup("", "", 3))

    @pytest.mark.parametrize("group_id, expectation",
    [
        (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_1, True),
        (TaskGroupDatabaseTestUtil.UNUSED_TASK_GROUP_ID, False),
        (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2, True),
    ])
    def test_is_group_registered(self, populated_task_group_inst, group_id: int, expectation: bool):
        assert populated_task_group_inst.is_group_registered(group_id) == expectation
