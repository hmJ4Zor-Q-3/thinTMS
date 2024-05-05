from threading import Thread

from werkzeug.serving import BaseWSGIServer


class ServerThread(Thread):
    def __init__(self, server: BaseWSGIServer):
        super().__init__()
        self.server = server

    def run(self) -> None:
        self.server.serve_forever()

    def kill(self) -> None:
        self.server.shutdown()
