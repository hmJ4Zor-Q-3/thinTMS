import pytest
from flask import Flask, current_app
from werkzeug.serving import make_server

from src.routes.flask_routes import IFlaskRoutes
from src.server.server_thread import ServerThread

HOST = "127.0.0.1"
PORT = 5000


# could use varargs, and change name to start_app_process
def start_app_process_with_endpoints(routes: IFlaskRoutes) -> ServerThread:
    """
    Creates and launches a flask server containg the specified route argument.
    Args:
        routes: The routes to be added.

    Returns: the active server, such that it may later be closed.

    """
    a = Flask(__name__)
    a.register_blueprint(routes.get_blueprint())

    p = ServerThread(make_server(HOST, PORT, a))
    p.start()
    return p


def close_app_process(app_process: ServerThread) -> None:
    """
    Shuts down a server thread.
    Args:
        app_process: The live server to be shut down.

    Returns: Nothing.

    """
    app_process.kill()
    app_process.join()


class FlaskTest:
    @pytest.fixture  # with's an option, but it would reduce choice: (autouse=True)
    def app_context(self):
        """
        Generates the necessary context for Response objects to be generated in.
        Returns: Nothing, simply invoking this fixture is all that is needed.

        """
        ac = Flask(__name__).app_context()
        ac.push()
        rc = current_app.test_request_context()
        rc.push()
        yield None
        rc.pop()
        ac.pop()
