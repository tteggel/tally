from ws4py.client.threadedclient import WebSocketClient
import requests
import socket
import json
from threading import Event
from subprocess import Popen
import unittest
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

        self.url = 'http://{0}:{1}/'.format(host, port)

        self.wait_ready()

        return self.url

    def stop(self):
        self.server_process.terminate()

    def wait_ready(self):
        tries = self.max_connect_tries
        while tries > 0:
            try:
                r = requests.get(self.url)
                if (r.status_code == 200):
                    break
            except:
                pass
            sleep(.1)
            tries = tries - 1

class TestWebSocket(unittest.TestCase):

    def test_websocket(self):
        with TestServer('server') as test_server:
            url = test_server.url
            new_response = requests.post(url + 'new', allow_redirects=False)
            tally_url = new_response.headers['Location']
            key = tally_url.split('/')[-1]
            ws_url = tally_url.replace('http', 'ws')

            next_expected_state = 1
            test = self
            ready = Event()

            class SendingClient(WebSocketClient):
                def send_inc(self, inc):
                    self.send(json.dumps({'message': 'inc',
                                          'key': key,
                                          'inc': inc}))

                def opened(self):
                    next_expected_state = 1
                    self.send_inc(1)

                    ready.wait()
                    next_expected_state = 0
                    self.send_inc(-1)

                    ready.wait()
                    next_expected_state = -1
                    self.send_inc(-1)

            class ListeningClient(WebSocketClient):
                def opened(self):
                    ws_two = SendingClient(ws_url)
                    ws_two.connect()

                def received_message(self, m):
                    print "here"
                    decoded = json.loads(str(m))
                    test.assertEqual(decoded['message'], 'changed')
                    test.assertEqual(decoded['value'], next_expected_state)
                    ready.set()

            ws_one = ListeningClient(ws_url)
            ws_one.connect()

if __name__ == '__main__':
    unittest.main()
