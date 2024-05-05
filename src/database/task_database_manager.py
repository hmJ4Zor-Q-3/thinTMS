from datetime import datetime

from src.data.task import Task
from src.data.unidentified_task import UnIDTask
from src.database.database_manager import DataBaseManager
from src.database.task_access import ITaskAccess
from src.database.task_group_access import ITaskGroupAccess
from src.database.task_group_database_manager import TaskGroupDatabaseManager
from src.database.user_database_manager import UserDatabaseManager


class TaskDatabaseManager(DataBaseManager, ITaskAccess):
    """A class to manage tasks stored in an SQLite database."""

    TASK_TABLE_NAME = "tasks"
    TASK_ID_COLUMN_NAME = "task_id"
    GROUP_ID_COLUMN_NAME = "group_id"
    TITLE_COLUMN_NAME = "title"
    DESCRIPTION_COLUMN_NAME = "description"
    DUE_DATE_COLUMN_NAME = "due_date"

    TITLE_LENGTH = 100

    def __init__(self, db_path: str, task_group_access: ITaskGroupAccess):
        super().__init__(db_path)
        self._tga = task_group_access
        self._initialize_db()

    def _initialize_db(self):
        with self.connection():
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {TaskDatabaseManager.TASK_TABLE_NAME} ("
                f"{TaskDatabaseManager.TASK_ID_COLUMN_NAME} INTEGER PRIMARY KEY, "
                f"{TaskDatabaseManager.GROUP_ID_COLUMN_NAME} INTEGER NOT NULL, "
                f"{TaskDatabaseManager.TITLE_COLUMN_NAME} VARCHAR({TaskDatabaseManager.TITLE_LENGTH}) NOT NULL, "
                f"{TaskDatabaseManager.DESCRIPTION_COLUMN_NAME} TEXT NOT NULL, "
                f"{TaskDatabaseManager.DUE_DATE_COLUMN_NAME} TEXT, "
                f"FOREIGN KEY({TaskDatabaseManager.GROUP_ID_COLUMN_NAME}) "
                f"  REFERENCES {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME}({TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME}))")

    def add_task(self, task: UnIDTask) -> Task:
        if not self._tga.is_group_registered(task.group_identifier):
            raise KeyError(f"Invalid group identifier: {task.group_identifier}.")

        with self.connection():
            self.cursor.execute(
                f"INSERT INTO {TaskDatabaseManager.TASK_TABLE_NAME} ({TaskDatabaseManager.GROUP_ID_COLUMN_NAME}, {TaskDatabaseManager.TITLE_COLUMN_NAME}, {TaskDatabaseManager.DESCRIPTION_COLUMN_NAME}, {TaskDatabaseManager.DUE_DATE_COLUMN_NAME}) "
                f"VALUES (?, ?, ?, ?)",
                (task.group_identifier, task.title, task.description, task.due_date.isoformat() if task.due_date is not None else None))
            self.conn.commit()
            return Task.of(task, self.cursor.lastrowid)

    def delete_task(self, task_id: int) -> None:
        if not self.is_task_registered(task_id):
            raise KeyError(f"Invalid task identifier: {task_id}.")

        with self.connection():
            self.cursor.execute(f"DELETE FROM {TaskDatabaseManager.TASK_TABLE_NAME} "
                                f"WHERE {TaskDatabaseManager.TASK_ID_COLUMN_NAME}=?",
                                (task_id,))
            self.conn.commit()

    def get_task(self, task_id: int) -> Task:
        if not self.is_task_registered(task_id):
            raise KeyError(f"Invalid task identifier: {task_id}.")

        with self.connection():
            t = self.cursor.execute(
                f"SELECT {TaskDatabaseManager.GROUP_ID_COLUMN_NAME}, {TaskDatabaseManager.TITLE_COLUMN_NAME}, {TaskDatabaseManager.DESCRIPTION_COLUMN_NAME}, {TaskDatabaseManager.DUE_DATE_COLUMN_NAME}, {TaskDatabaseManager.TASK_ID_COLUMN_NAME} "
                f"FROM {TaskDatabaseManager.TASK_TABLE_NAME} "
                f"WHERE {TaskDatabaseManager.TASK_ID_COLUMN_NAME}=?", (task_id,)).fetchone()

            return Task(t[0], t[1], t[2], t[3] if t[3] is None else datetime.fromisoformat(t[3]), t[4])

    def get_tasks(self, group_id: int) -> list[Task]:
        if not self._tga.is_group_registered(group_id):
            raise KeyError(f"Invalid group identifier: {group_id}.")

        with self.connection():
            ts = self.cursor.execute(
                f"SELECT {TaskDatabaseManager.GROUP_ID_COLUMN_NAME}, {TaskDatabaseManager.TITLE_COLUMN_NAME}, {TaskDatabaseManager.DESCRIPTION_COLUMN_NAME}, {TaskDatabaseManager.DUE_DATE_COLUMN_NAME}, {TaskDatabaseManager.TASK_ID_COLUMN_NAME} "
                f"FROM {TaskDatabaseManager.TASK_TABLE_NAME} "
                f"WHERE {TaskDatabaseManager.GROUP_ID_COLUMN_NAME}=?",
                (group_id,)
            ).fetchall()
            return [Task(t[0], t[1], t[2], t[3] if t[3] is None else datetime.fromisoformat(t[3]), t[4]) for t in ts]

    def update_task(self, task: Task) -> None:
        if not self.is_task_registered(task.identifier):
            raise KeyError(f"Invalid task identifier: {task.identifier}.")

        with self.connection():
            self.cursor.execute(
                f"UPDATE {TaskDatabaseManager.TASK_TABLE_NAME} "
                f"SET {TaskDatabaseManager.TITLE_COLUMN_NAME}=?, "
                f"  {TaskDatabaseManager.DESCRIPTION_COLUMN_NAME}=?, "
                f"  {TaskDatabaseManager.DUE_DATE_COLUMN_NAME}=? "
                f"WHERE {TaskDatabaseManager.TASK_ID_COLUMN_NAME}=?",
                (task.title, task.description, task.due_date.isoformat() if task.due_date is not None else None, task.identifier))
            self.conn.commit()

    def is_task_registered(self, task_id: int) -> bool:
        with self.connection():
            return len(self.cursor.execute(
                f"SELECT {TaskDatabaseManager.TASK_ID_COLUMN_NAME} "
                f"FROM {TaskDatabaseManager.TASK_TABLE_NAME} "
                f"WHERE {TaskDatabaseManager.TASK_ID_COLUMN_NAME}=?",
                (task_id,))
                       .fetchall()) == 1
