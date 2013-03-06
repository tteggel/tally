from threading import Condition, Event
from ws4py.client.threadedclient import WebSocketClient, WebSocketBaseClient
import requests
import json
import unittest

from utils import TestServer

class TestWebSocket(unittest.TestCase):
    TIMEOUT = 5

    def test_websocket(self):
        with TestServer('server') as test_server:
            url = test_server.url
            new_response = requests.post(url + 'new',
                                         allow_redirects=False,
                                         verify=False)
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
                    if len(results) == 4: fin.set()

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
