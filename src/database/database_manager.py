import sqlite3
from sqlite3 import Connection, Cursor


# capitalization is intentional, it's only meant as a base class
class DataBaseManager:
    def __init__(self, db_path: str):
        """

        Args:
            db_path: The path to find or create the database at.
        """
        self.db_path = db_path
        self.cursor = None  # type: Cursor
        self.conn = None  # type: Connection

    def connection(self) -> object:
        """Create an object that will open and close the database connection in a with statement."""
        class _:
            def __init__(self, parent):
                self.parent = parent

            def __enter__(self):
                self.parent.conn = sqlite3.connect(self.parent.db_path)
                self.parent.cursor = self.parent.conn.cursor()

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.parent.conn.close()
                self.parent.conn = None
                self.parent.cursor = None

        return _(self)
