from flask import Flask

from src.database.task_database_manager import TaskDatabaseManager
from src.database.task_group_database_manager import TaskGroupDatabaseManager
from src.database.user_database_manager import UserDatabaseManager
from src.routes.auth_routes import UserApi
from src.routes.implementation.tms_task_implementation import TMSTaskApiImpl
from src.routes.implementation.tms_user_implementation import TMSUserApiImpl
from src.routes.task_routes import TaskApi
from src.routes.website_routes import TMSWebsiteRoutes
from src.security.security import TMSSecurityStandard


class TMSServer:
    def __init__(self, database_path: str):
        self.database_path = database_path

        self.ss = TMSSecurityStandard()

        self.u_db = UserDatabaseManager(self.database_path, self.ss)
        self.tg_db = TaskGroupDatabaseManager(self.database_path, self.u_db)
        self.t_db = TaskDatabaseManager(self.database_path, self.tg_db)

        self.app = Flask(__name__,
                         template_folder=TMSWebsiteRoutes.TEMPLATES_PATH,
                         static_folder=TMSWebsiteRoutes.STATIC_PATH)

        self.app.register_blueprint(UserApi(TMSUserApiImpl(self.u_db, self.ss)).get_blueprint())
        self.app.register_blueprint(TaskApi(TMSTaskApiImpl(self.u_db, self.tg_db, self.t_db)).get_blueprint())

        self.app.register_blueprint(TMSWebsiteRoutes(
            UserDatabaseManager.USERNAME_LENGTH,
            TMSSecurityStandard.PASSWORD_MIN_LENGTH).get_blueprint())

    def get_app(self):
        return self.app


def main():
    TMSServer("database.db").get_app().run()#ssl_context='adhoc')


if __name__ == "__main__":
    main()
