import random
import string
from datetime import datetime, timedelta

import pytest

from src.data.serialization.json.task_serializer import TaskSerializer
from src.data.task import Task
from src.exceptions.invalid_state_error import InvalidStateError
from src.routes.task_routes import TaskApi


class TestTaskSerializer:
    @pytest.fixture
    def random_task(self):
        g_id = random.randint(-pow(2, 16), pow(2, 16))
        t = "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=random.randint(0, pow(2, 8))))
        d = "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=random.randint(0, pow(2, 10))))
        min_date = datetime(1, 1, 1, 1, 0, 0)
        max_date = datetime(9999, 12, 31, 23, 59, 59)
        dd = None if random.randint(0, 1) == 0 else min_date + timedelta(days=random.randint(0, (max_date - min_date).days))
        t_id = random.randint(-pow(2, 16), pow(2, 16))

        return Task(g_id, t, d, dd, t_id)

    @pytest.fixture
    def serializer(self):
        return TaskSerializer()

    def test_start_failure(self, serializer, random_task):
        serializer.start(random_task)
        with pytest.raises(InvalidStateError):
            serializer.start(random_task)

    def test_drop_group_identifier(self, serializer, random_task):
        js = serializer.start(random_task).drop_group_identifier().end()

        assert TaskApi.GROUP_ID_KEY not in js
        assert js[TaskApi.TASK_TITLE_KEY] == random_task.title
        assert js[TaskApi.TASK_DESCRIPTION_KEY] == random_task.description
        assert random_task.due_date is None or js[TaskApi.TASK_DATE_KEY] == random_task.due_date.isoformat()
        assert js[TaskApi.TASK_ID_KEY] == random_task.identifier

    def test_drop_identifier(self, serializer, random_task):
        js = serializer.start(random_task).drop_identifier().end()

        assert js[TaskApi.GROUP_ID_KEY] == random_task.group_identifier
        assert js[TaskApi.TASK_TITLE_KEY] == random_task.title
        assert js[TaskApi.TASK_DESCRIPTION_KEY] == random_task.description
        assert random_task.due_date is None or js[TaskApi.TASK_DATE_KEY] == random_task.due_date.isoformat()
        assert TaskApi.TASK_ID_KEY not in js

    def test_drop_description(self, serializer, random_task):
        js = serializer.start(random_task).drop_description().end()

        assert js[TaskApi.GROUP_ID_KEY] == random_task.group_identifier
        assert js[TaskApi.TASK_TITLE_KEY] == random_task.title
        assert TaskApi.TASK_DESCRIPTION_KEY not in js
        assert random_task.due_date is None or js[TaskApi.TASK_DATE_KEY] == random_task.due_date.isoformat()
        assert js[TaskApi.TASK_ID_KEY] == random_task.identifier

    def test_end(self, serializer, random_task):
        js = serializer.start(random_task).end()

        assert js[TaskApi.GROUP_ID_KEY] == random_task.group_identifier
        assert js[TaskApi.TASK_TITLE_KEY] == random_task.title
        assert js[TaskApi.TASK_DESCRIPTION_KEY] == random_task.description
        assert random_task.due_date is None or js[TaskApi.TASK_DATE_KEY] == random_task.due_date.isoformat()
        assert js[TaskApi.TASK_ID_KEY] == random_task.identifier
