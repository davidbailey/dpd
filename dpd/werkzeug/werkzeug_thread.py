import webbrowser
from threading import Thread

from werkzeug.serving import make_server


class WerkzeugThread(Thread):
    def __init__(self, app, hostname="localhost", port=9000):
        super().__init__()
        self.hostname = hostname
        self.port = port
        self.server = make_server(self.hostname, self.port, app)

    def run(self, open_webbrowser=True):
        if open_webbrowser:
            webbrowser.open("http://" + self.hostname + ":" + str(self.port))
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
