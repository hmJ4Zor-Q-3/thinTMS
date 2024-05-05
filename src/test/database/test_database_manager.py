import pytest

from src.database.database_manager import DataBaseManager
from src.test.database.util.database_test_util import DatabaseTestUtil


class TestDataBaseManager(DatabaseTestUtil):
    @pytest.fixture
    def inst(self, test_path):
        return DataBaseManager(test_path)

    def test__connection(self, inst):
        with inst.connection():
            assert inst.conn is not None
            assert inst.cursor is not None

        assert inst.conn is None
        assert inst.cursor is None
