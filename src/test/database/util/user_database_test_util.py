import binascii
import datetime

import pytest

from src.database.user_database_manager import UserDatabaseManager
from src.security.security import TMSSecurityStandard
from src.test.database.util.database_test_util import DatabaseTestUtil


class UserDatabaseTestUtil(DatabaseTestUtil):
    SS = TMSSecurityStandard()

    USERNAME_1 = "O"
    PASSWORD_1 = "@l93#3kcF$J*elM$LS:"
    PASSWORD_1_HASH = SS.hash(PASSWORD_1)
    TOKEN_1 = binascii.unhexlify("25cbc605fa25a6357d2d7f7d734532418b6e4d032f0db51782adec51af0deff3")

    USERNAME_2 = "ABCDEFgees"
    PASSWORD_2 = "3d_3k!~|d_k3l-;feTs"
    PASSWORD_2_HASH = SS.hash(PASSWORD_2)

    USERNAME_3 = "L"
    PASSWORD_3 = ":-O30Pkl@$dlL"
    PASSWORD_3_HASH = SS.hash(PASSWORD_3)
    TOKEN_3 = binascii.unhexlify("f936c3a7b1e9bc4eb072012bda1500efee41909210dbdc83b85855191ab86cde")
    SS = None

    UNUSED_USERNAME = "jhg"

    @pytest.fixture
    def user_inst(self, test_path):
        return UserDatabaseManager(test_path, TMSSecurityStandard())

    @pytest.fixture
    def populated_user_inst(self, user_inst):
        pcn = f"({UserDatabaseManager.USERNAME_COLUMN_NAME}, {UserDatabaseManager.PASSWORD_COLUMN_NAME})"
        ecn = f"({UserDatabaseManager.USERNAME_COLUMN_NAME}, {UserDatabaseManager.PASSWORD_COLUMN_NAME}, {UserDatabaseManager.AUTH_TOKEN_COLUMN_NAME}, {UserDatabaseManager.TOKEN_EXPIRY_COLUMN_NAME})"

        def exp():
            return (datetime.timedelta(hours=6) + datetime.datetime.now()).isoformat()

        with user_inst.connection():
            user_inst.cursor.execute(f"INSERT INTO {UserDatabaseManager.USER_TABLE_NAME} {ecn} VALUES (?, ?, ?, ?)", (UserDatabaseTestUtil.USERNAME_1, binascii.hexlify(UserDatabaseTestUtil.PASSWORD_1_HASH), binascii.hexlify(UserDatabaseTestUtil.TOKEN_1), exp(),))
            user_inst.cursor.execute(f"INSERT INTO {UserDatabaseManager.USER_TABLE_NAME} {pcn} VALUES (?, ?)", (UserDatabaseTestUtil.USERNAME_2, binascii.hexlify(UserDatabaseTestUtil.PASSWORD_2_HASH),))
            user_inst.cursor.execute(f"INSERT INTO {UserDatabaseManager.USER_TABLE_NAME} {ecn} VALUES (?, ?, ?, ?)", (UserDatabaseTestUtil.USERNAME_3, binascii.hexlify(UserDatabaseTestUtil.PASSWORD_3_HASH), binascii.hexlify(UserDatabaseTestUtil.TOKEN_3), exp(),))
            user_inst.conn.commit()
        return user_inst
