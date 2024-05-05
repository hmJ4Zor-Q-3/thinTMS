import pytest

from src.data.task_group import TaskGroup
from src.database.task_group_database_manager import TaskGroupDatabaseManager
from src.test.database.util.user_database_test_util import UserDatabaseTestUtil


class TaskGroupDatabaseTestUtil(UserDatabaseTestUtil):
    TASK_GROUP_ID_1 = 1
    TASK_GROUP_USERNAME_1 = UserDatabaseTestUtil.USERNAME_3
    TASK_GROUP_NAME_1 = "ctrl4m"
    TASK_GROUP_1 = TaskGroup(TASK_GROUP_USERNAME_1, TASK_GROUP_NAME_1, TASK_GROUP_ID_1)

    TASK_GROUP_ID_2 = 3
    TASK_GROUP_USERNAME_2 = UserDatabaseTestUtil.USERNAME_1
    TASK_GROUP_NAME_2 = ""
    TASK_GROUP_2 = TaskGroup(TASK_GROUP_USERNAME_2, TASK_GROUP_NAME_2, TASK_GROUP_ID_2)

    TASK_GROUP_ID_3 = 2
    TASK_GROUP_USERNAME_3 = UserDatabaseTestUtil.USERNAME_3
    TASK_GROUP_NAME_3 = "_"
    TASK_GROUP_3 = TaskGroup(TASK_GROUP_USERNAME_3, TASK_GROUP_NAME_3, TASK_GROUP_ID_3)

    TASK_GROUP_GROUPS = [TASK_GROUP_1, TASK_GROUP_2, TASK_GROUP_3]

    USERNAME_1_GROUPS = [TASK_GROUP_2]
    USERNAME_2_GROUPS = []
    USERNAME_3_GROUPS = [TASK_GROUP_1, TASK_GROUP_3]

    UNUSED_TASK_GROUP_ID = 90

    @pytest.fixture
    def task_group_inst(self, test_path, populated_user_inst):
        return TaskGroupDatabaseManager(test_path, populated_user_inst)

    @pytest.fixture
    def populated_task_group_inst(self, task_group_inst):
        with task_group_inst.connection():
            colm_lst = f"({TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME}, {TaskGroupDatabaseManager.USERNAME_COLUMN_NAME}, {TaskGroupDatabaseManager.NAME_COLUMN_NAME})"
            task_group_inst.cursor.execute(
                f"INSERT INTO {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} {colm_lst} VALUES (?, ?, ?)",
                (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_1, TaskGroupDatabaseTestUtil.TASK_GROUP_USERNAME_1, TaskGroupDatabaseTestUtil.TASK_GROUP_NAME_1))
            task_group_inst.cursor.execute(
                f"INSERT INTO {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} {colm_lst} VALUES (?, ?, ?)",
                (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2, TaskGroupDatabaseTestUtil.TASK_GROUP_USERNAME_2, TaskGroupDatabaseTestUtil.TASK_GROUP_NAME_2))
            task_group_inst.cursor.execute(
                f"INSERT INTO {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} {colm_lst} VALUES (?, ?, ?)",
                (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_3, TaskGroupDatabaseTestUtil.TASK_GROUP_USERNAME_3, TaskGroupDatabaseTestUtil.TASK_GROUP_NAME_3))
            task_group_inst.conn.commit()

        return task_group_inst
