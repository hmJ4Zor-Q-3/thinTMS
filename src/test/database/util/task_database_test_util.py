from datetime import datetime

import pytest

from src.data.task import Task
from src.database.task_database_manager import TaskDatabaseManager
from src.test.database.util.task_group_database_test_util import TaskGroupDatabaseTestUtil


class TaskDatabaseTestUtil(TaskGroupDatabaseTestUtil):
    TASK_1 = Task(TaskGroupDatabaseTestUtil.TASK_GROUP_ID_3, "", "Paint socks", None, 0)
    TASK_2 = Task(TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2, "title", "desc", datetime.now(), 1)
    TASK_3 = Task(TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2, "1. ", "9", None, 13)

    TASKS = [TASK_1, TASK_2, TASK_3]

    UNUSED_TASK_ID_1 = 20
    UNUSED_TASK_ID_2 = 12

    @pytest.fixture
    def task_inst(self, test_path, populated_task_group_inst):
        return TaskDatabaseManager(test_path, populated_task_group_inst)

    @pytest.fixture
    def populated_task_inst(self, task_inst):
        with task_inst.connection():
            colm_ord = f"({TaskDatabaseManager.GROUP_ID_COLUMN_NAME}, {TaskDatabaseManager.TITLE_COLUMN_NAME}, {TaskDatabaseManager.DESCRIPTION_COLUMN_NAME}, {TaskDatabaseManager.DUE_DATE_COLUMN_NAME}, {TaskDatabaseManager.TASK_ID_COLUMN_NAME})"

            for task in TaskDatabaseTestUtil.TASKS:
                task_inst.cursor.execute(
                    f"INSERT INTO {TaskDatabaseManager.TASK_TABLE_NAME} {colm_ord} "
                    f"VALUES (?, ?, ?, ?, ?)",
                    (task.group_identifier, task.title, task.description,
                     task.due_date.isoformat() if task.due_date is not None else None, task.identifier))

            task_inst.conn.commit()

        return task_inst
