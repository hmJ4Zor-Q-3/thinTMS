import os

from werkzeug.serving import make_server

from src.exceptions.invalid_state_error import InvalidStateError
from src.server.server_thread import ServerThread
from src.server.tms_server import TMSServer


database_path = None    # type: str
server = None   # type: ServerThread


def start_server(host, port, db_path):
    global server
    global database_path
    if server is not None:
        raise InvalidStateError("Server already running.")

    database_path = db_path
    server = ServerThread(make_server(host, port, TMSServer(db_path).get_app()))
    print(server)
    server.start()


def close_server():
    global server
    global database_path
    print(server)
    if server is None:
        raise InvalidStateError("No server running.")

    server.kill()
    server.join()
    server = None
    os.remove(database_path)
