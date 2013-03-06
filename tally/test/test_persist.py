import requests
import json
import unittest

from utils import TestServer

class TestWebSocket(unittest.TestCase):
    TIMEOUT = 5

    def test_persistent_key(self):
        """
        Check that the persistence layer is working by starting a server,
        creating a new key and then seeing if we can get that key from
        a second server instance.
        """
        key = None
        with TestServer('server') as test_server1:
            url = test_server1.url
            new_response = requests.post(url + 'new',
                                         allow_redirects=False,
                                         verify=False)
            tally_url = new_response.headers['Location']
            key = tally_url.split('/')[-1]
            requests.post(tally_url + '/inc', data={'inc': '234560'},
                          verify=False)

        with TestServer('server') as test_server2:
            url = test_server2.url
            new_response = requests.get(url + key, verify=False)

        self.assertIn('234560', new_response.text)

if __name__ == '__main__':
    unittest.main()
