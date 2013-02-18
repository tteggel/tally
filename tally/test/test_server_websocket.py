from websocket import create_connection
import requests
import tl.testing.thread
from tl.testing.thread import ThreadAwareTestCase, ThreadJoiner
import socket
import json
from threading import Event
from time import sleep
from subprocess import Popen
import unittest
import os

import tally.server

class TestServer():
    def __init__(self, app):
        self.app = app

    def start(self):
        def find_endpoint():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 0))
            host, port = s.getsockname()
            s.close()
            return '127.0.0.1', port

        host, port = find_endpoint()

        with open(os.devnull, 'w') as devnull:
            self.server_process = Popen(['python', self.app.__file__,
                                         '-a', host,
                                         '-p', str(port)])#,
                                        #stdout=devnull, stderr=devnull)

        self.url = 'http://{0}:{1}/'.format(host, port)

        self.wait_ready()

        return self.url

    def stop(self):
        self.server_process.terminate()

    def wait_ready(self):
        while True:
            r = requests.get(self.url)
            if (r.status_code == 200):
                break
            sleep(.1)


class TestWebSocket(ThreadAwareTestCase):

    def test_websockets(self):
        with ThreadJoiner(1):
            test_server = TestServer(tally.server)
            url = test_server.start()

            new_response = requests.post(url + 'new', allow_redirects=False)
            tally_url = new_response.headers['Location']
            key = tally_url.split('/')[-1]
            ws_url = tally_url.replace('http', 'ws')

            # first client
            ws_one = create_connection(ws_url)

            ready = Event()

            def second_client():
                ws_two = create_connection(ws_url)
                ready.set()
                message = ws_two.recv()
                decoded = json.loads(message)
                self.assertEqual(decoded['message'], 'changed')

            self.run_in_thread(second_client)

            ready.wait()
            ws_one.send(json.dumps({'message': 'inc',
                                    'key': key,
                                    'inc': '1'}))

        test_server.stop()

    def test_websocket_zero_message_bug(self):
        with ThreadJoiner(1):
            test_server = TestServer(tally.server)
            url = test_server.start()

            new_response = requests.post(url + 'new', allow_redirects=False)
            tally_url = new_response.headers['Location']
            key = tally_url.split('/')[-1]
            ws_url = tally_url.replace('http', 'ws')

            # first client
            ws_one = create_connection(ws_url)

            ready = Event()

            def second_client():
                ws_two = create_connection(ws_url)
                ready.set()
                message = ws_two.recv()
                decoded = json.loads(message)
                self.assertEqual(decoded['message'], 'changed')
                self.assertEqual(decoded['value'], 1)

                ready.set()
                message = ws_two.recv()
                decoded = json.loads(message)
                self.assertEqual(decoded['message'], 'changed')
                self.assertEqual(decoded['value'], 0)

            self.run_in_thread(second_client)

            ready.wait()
            ws_one.send(json.dumps({'message': 'inc',
                                    'key': key,
                                    'inc': '1'}))

            ready.wait()
            ws_one.send(json.dumps({'message': 'inc',
                                    'key': key,
                                    'inc': '-1'}))

        test_server.stop()

if __name__ == '__main__':
    unittest.main()
