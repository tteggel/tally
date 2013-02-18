from webtest import TestApp
from websocket import create_connection
import server
import unittest

class TestServer(unittest.TestCase):
    def setUp(self):
        self.testapp = TestApp(server.app)

    def test_index(self):
        assert self.testapp.get('/').status == '200 OK'

    def test_can_create_new_tally_from_index(self):
        index_response = self.testapp.get('/')
        assert 'action="new"' in index_response
        assert '<button type="submit"' in index_response

    def test_404_from_unknown_key(self):
        self.testapp.get('/dartmoor', status=404)

    def test_new_key(self):
        new_response = self.testapp.post('/new', status=302)
        assert 'Location' in new_response.headers
        self.assertEqual(new_response.status, '302 Found')
        tally_response = new_response.follow()

    def test_two_new_keys(self):
        new_response_one = self.testapp.post('/new', status=302)
        tally_one_url = new_response_one.headers['Location']

        new_response_two = self.testapp.post('/new', status=302)
        tally_two_url = new_response_two.headers['Location']

        self.assertNotEqual(tally_one_url, tally_two_url)

if __name__ == '__main__':
    unittest.main()
