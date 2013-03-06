import requests
from requests import ConnectionError
import socket
from subprocess import Popen
import os
from time import sleep

class TestServer():
    def __init__(self, file, max_connect_tries=60):
        self.file = '{0}/../{1}.py'.format(os.path.dirname(__file__), file)
        self.max_connect_tries = max_connect_tries

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        def find_endpoint():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 0))
            host, port = s.getsockname()
            s.close()
            return '127.0.0.1', port

        host, port = find_endpoint()

        with open(os.devnull, 'w') as devnull:
            self.server_process = Popen(['python', self.file,
                                         '-a', host,
                                         '-p', str(port)],
                                        stderr=devnull, stdout=devnull)

        self.url = 'https://{0}:{1}/'.format(host, port)

        self.wait_ready()

        return self.url

    def stop(self):
        self.server_process.terminate()

    def wait_ready(self):
        tries = self.max_connect_tries
        while tries > 0:
            try:
                r = requests.get(self.url, verify=False)
                if (r.status_code == 200):
                    break
            except ConnectionError:
                pass

            sleep(.1)
            tries = tries - 1

        if tries == 0: raise ConnectionError
