from threading import Condition, Event
from ws4py.client.threadedclient import WebSocketClient, WebSocketBaseClient
import requests
import socket
import json
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
    TIMEOUT = 5

    def test_websocket(self):
        with TestServer('server') as test_server:
            url = test_server.url
            new_response = requests.post(url + 'new',
                                         allow_redirects=False)
            tally_url = new_response.headers['Location']
            key = tally_url.split('/')[-1]
            ws_url = tally_url.replace('http', 'ws')

            results = []

            # ready to send a message?
            ready = Condition()

            # finished?
            fin = Event()

            class SendingClient(WebSocketClient):
                def send_inc(self, inc, expected=0):
                    ready.acquire()
                    ready.wait(TestWebSocket.TIMEOUT)
                    self.send(json.dumps({'message': 'inc',
                                          'key': key,
                                          'inc': inc}))
                    ready.release()

                def opened(self):
                    # 0 + 1 = 1
                    self.send_inc(1, expected=1)

                    # 1 - 1 = 0
                    self.send_inc(-1, expected=0)

                    # 0 - 1 = -1
                    self.send_inc(-1, expected=-1)

                    # -1 + 1 = 0
                    self.send_inc(1, expected=0)

                    fin.set()

            class ListeningClient(WebSocketClient):
                def opened(self):
                    self.ws_two = SendingClient(ws_url)
                    self.ws_two.connect()

                def received_message(self, m):
                    ready.acquire()
                    decoded = json.loads(str(m))
                    result = decoded
                    results.append(result)
                    ready.notify()
                    ready.release()

            ws_one = ListeningClient(ws_url)
            ws_one.connect()

            # signal ready to send the first message.
            ready.acquire(); ready.notify(); ready.release()

            # wait for the end
            self.assertTrue(fin.wait(TestWebSocket.TIMEOUT))

            # check the results
            self.assertEqual(len(results), 4)

            for result in results: self.assertEqual(result['message'], 'changed')

            self.assertEqual([1, 0, -1, 0],
                             [result['value'] for result in results])

if __name__ == '__main__':
    unittest.main()
