from src.data.task_group import TaskGroup
from src.data.unidentified_task_group import UnIDTaskGroup
from src.database.database_manager import DataBaseManager
from src.database.task_group_access import ITaskGroupAccess
from src.database.user_access import IUserAccess
from src.database.user_database_manager import UserDatabaseManager
from src.exceptions.exceptions import UsernameError


class TaskGroupDatabaseManager(DataBaseManager, ITaskGroupAccess):
    """A class to manage task groups stored in an SQLite database."""

    TASK_GROUP_TABLE_NAME = "task_groups"
    GROUP_ID_COLUMN_NAME = "group_id"
    USERNAME_COLUMN_NAME = "username"
    NAME_COLUMN_NAME = "name"

    NAME_LENGTH = 50

    def __init__(self, db_path: str, user_access: IUserAccess):
        super().__init__(db_path)
        self._ua = user_access
        self._initialize_db()

    def _initialize_db(self):
        with self.connection():
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} ("
                f"{TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME} INTEGER PRIMARY KEY, "
                f"{TaskGroupDatabaseManager.USERNAME_COLUMN_NAME} TEXT NOT NULL, "
                f"{TaskGroupDatabaseManager.NAME_COLUMN_NAME} VARCHAR({TaskGroupDatabaseManager.NAME_LENGTH}) NOT NULL, "
                f"FOREIGN KEY({TaskGroupDatabaseManager.USERNAME_COLUMN_NAME}) "
                f"  REFERENCES {UserDatabaseManager.USER_TABLE_NAME}({UserDatabaseManager.USERNAME_COLUMN_NAME}))")

    def add_task_group(self, task_group: UnIDTaskGroup) -> TaskGroup:
        if not self._ua.is_user_registered(task_group.username):
            raise UsernameError(f"User: {task_group.username}, does not exist")

        with self.connection():
            self.cursor.execute(
                f"INSERT INTO {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} "
                f"({TaskGroupDatabaseManager.USERNAME_COLUMN_NAME}, {TaskGroupDatabaseManager.NAME_COLUMN_NAME}) "
                f"VALUES (?, ?)",
                (task_group.username, task_group.name,))
            self.conn.commit()
            return TaskGroup.of(task_group, self.cursor.lastrowid)

    def delete_task_group(self, group_id: int) -> None:
        if not self.is_group_registered(group_id):
            raise KeyError(f"Invalid group identifier: {group_id}.")

        with self.connection():
            self.cursor.execute(f"DELETE FROM {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} "
                                f"WHERE {TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME}=?",
                                (group_id,))
            self.conn.commit()

    def get_task_group(self, group_id: int) -> TaskGroup:
        if not self.is_group_registered(group_id):
            raise KeyError(f"Invalid group identifier: {group_id}.")

        with self.connection():
            t = self.cursor.execute(
                f"SELECT {TaskGroupDatabaseManager.USERNAME_COLUMN_NAME}, {TaskGroupDatabaseManager.NAME_COLUMN_NAME}, {TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME} "
                f"FROM {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} "
                f"WHERE {TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME}=?",
                (group_id,)).fetchone()
            return TaskGroup(t[0], t[1], t[2])

    def get_task_groups(self, username: str) -> list[TaskGroup]:
        if not self._ua.is_user_registered(username):
            raise UsernameError(f"User: {username}, does not exist")

        with self.connection():
            s = self.cursor.execute(
                f"SELECT {TaskGroupDatabaseManager.USERNAME_COLUMN_NAME}, {TaskGroupDatabaseManager.NAME_COLUMN_NAME}, {TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME} "
                f"FROM {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} "
                f"WHERE {TaskGroupDatabaseManager.USERNAME_COLUMN_NAME}=?",
                (username,)).fetchall()
            return [TaskGroup(t[0], t[1], t[2]) for t in s]

    def update_task_group(self, task_group: TaskGroup) -> None:
        if not self.is_group_registered(task_group.identifier):
            raise KeyError(f"Invalid group identifier: {task_group.identifier}.")

        with self.connection():
            self.cursor.execute(
                f"UPDATE {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} "
                f"SET {TaskGroupDatabaseManager.NAME_COLUMN_NAME}=? "
                f"WHERE {TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME}=?",
                (task_group.name, task_group.identifier))
            self.conn.commit()

    def is_group_registered(self, group_id: int) -> bool:
        with (self.connection()):
            return len(self.cursor.execute(
                f"SELECT {TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME} "
                f"FROM {TaskGroupDatabaseManager.TASK_GROUP_TABLE_NAME} "
                f"WHERE {TaskGroupDatabaseManager.GROUP_ID_COLUMN_NAME}=?",
                (group_id,))
                       .fetchall()) == 1
