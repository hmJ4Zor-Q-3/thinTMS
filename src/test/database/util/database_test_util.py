import os

import pytest


class DatabaseTestUtil:
    PATH = "src/test/test_database.db"

    @pytest.fixture
    def test_path(self):
        yield DatabaseTestUtil.PATH
        os.remove(DatabaseTestUtil.PATH)
