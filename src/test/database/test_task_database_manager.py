from datetime import datetime

import pytest

from src.data.task import Task
from src.data.unidentified_task import UnIDTask
from src.database.task_database_manager import TaskDatabaseManager
from src.test.database.util.task_database_test_util import TaskDatabaseTestUtil
from src.test.database.util.task_group_database_test_util import TaskGroupDatabaseTestUtil


class TestTaskDatabaseManager(TaskDatabaseTestUtil):

    def test___init__(self, task_inst):
        with task_inst.connection():
            assert len(task_inst.cursor.execute(
                "SELECT name "
                "FROM sqlite_master "
                "WHERE type='table' AND name=?",
                (TaskDatabaseManager.TASK_TABLE_NAME,)).fetchall()) == 1

    @pytest.mark.parametrize("task", [
        UnIDTask(TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2, "ttl,", "Do something", datetime(2015, 1, 1)),
        UnIDTask(TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2, "", "D---------------------l3; o", None),
        UnIDTask(TaskGroupDatabaseTestUtil.TASK_GROUP_ID_3, "ttl,", "", datetime.fromisoformat("2031-12-30T01:20:42Z"))
    ])
    def test_add_task(self, task_inst, task: UnIDTask):
        t = task_inst.add_task(task)
        assert task_inst.is_task_registered(t.identifier)
        task = Task.of(task, t.identifier)
        assert t == task
        t = task_inst.get_task(t.identifier)
        assert t == task

    def test_add_task_invalid_group(self, task_inst):
        with pytest.raises(KeyError):
            task_inst.add_task(UnIDTask(TaskGroupDatabaseTestUtil.UNUSED_TASK_GROUP_ID, "", "", None))

    @pytest.mark.parametrize("task_id", [
        TaskDatabaseTestUtil.TASK_1.identifier,
        TaskDatabaseTestUtil.TASK_1.identifier,
        TaskDatabaseTestUtil.TASK_2.identifier
    ])
    def test_delete_task(self, populated_task_inst, task_id: int):
        assert populated_task_inst.is_task_registered(task_id)
        populated_task_inst.delete_task(task_id)
        assert not populated_task_inst.is_task_registered(task_id)

    @pytest.mark.parametrize("task_id", [
        -190, -1, 0, 1, 2203])
    def test_delete_task_invalid_task(self, task_inst, task_id: int):
        with pytest.raises(KeyError):
            task_inst.delete_task(task_id)

    @pytest.mark.parametrize("task_id, expectation", [
        (TaskDatabaseTestUtil.TASK_1.identifier, TaskDatabaseTestUtil.TASK_1),
        (TaskDatabaseTestUtil.TASK_2.identifier, TaskDatabaseTestUtil.TASK_2)
    ])
    def test_get_task(self, populated_task_inst, task_id: int, expectation: Task):
        assert populated_task_inst.get_task(task_id) == expectation

    @pytest.mark.parametrize("task_id", [
        -190, -1, 0, 1, 2203])
    def test_get_task_invalid_task(self, task_inst, task_id: int):
        with pytest.raises(KeyError):
            task_inst.get_task(task_id)

    @pytest.mark.parametrize("group_id, expectation", [
        (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_1, [t for t in TaskDatabaseTestUtil.TASKS if t.group_identifier == TaskGroupDatabaseTestUtil.TASK_GROUP_ID_1]),
        (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_3, [t for t in TaskDatabaseTestUtil.TASKS if t.group_identifier == TaskGroupDatabaseTestUtil.TASK_GROUP_ID_3]),
        (TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2, [t for t in TaskDatabaseTestUtil.TASKS if t.group_identifier == TaskGroupDatabaseTestUtil.TASK_GROUP_ID_2]),
    ])
    def test_get_tasks(self, populated_task_inst, group_id: int, expectation: list[Task]):
        assert populated_task_inst.get_tasks(group_id) == expectation

    def test_get_tasks_invalid_group(self, task_inst):
        with pytest.raises(KeyError):
            task_inst.get_tasks(TaskGroupDatabaseTestUtil.UNUSED_TASK_GROUP_ID)

    @pytest.mark.parametrize("task", [
        Task(TaskDatabaseTestUtil.TASK_1.group_identifier, TaskDatabaseTestUtil.TASK_1.title, TaskDatabaseTestUtil.TASK_1.description, datetime.now(), TaskDatabaseTestUtil.TASK_1.identifier),  # test only change of date
        Task(TaskDatabaseTestUtil.TASK_2.group_identifier, "", "", None, TaskDatabaseTestUtil.TASK_2.identifier)  # test blanking out all data
    ])
    def test_update_task(self, populated_task_inst, task: Task):
        populated_task_inst.update_task(task)
        assert populated_task_inst.get_task(task.identifier) == task

    def test_update_task_invalid_task(self, task_inst):
        with pytest.raises(KeyError):
            task_inst.update_task(Task(0, "tlf-le", "[d]", datetime.now(), 57))

    @pytest.mark.parametrize("task_id, expectation", [
        (TaskDatabaseTestUtil.TASK_1.identifier, True),
        (TaskDatabaseTestUtil.UNUSED_TASK_ID_2, False),
        (TaskDatabaseTestUtil.TASK_2.identifier, True),
        (TaskDatabaseTestUtil.UNUSED_TASK_ID_1, False)
    ])
    def test_is_task_registered(self, populated_task_inst, task_id: int, expectation: bool):
        assert populated_task_inst.is_task_registered(task_id) == expectation

    # TODO, there may be inputs that violate the type hints and can break the application/database
