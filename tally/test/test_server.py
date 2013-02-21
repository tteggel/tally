from webtest import TestApp
import unittest

import tally.server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.testapp = TestApp(tally.server.app)

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

    def test_three_new_keys(self):
        new_response_one = self.testapp.post('/new', status=302)
        tally_one_url = new_response_one.headers['Location']
        new_response_one.follow()

        new_response_two = self.testapp.post('/new', status=302)
        tally_two_url = new_response_two.headers['Location']
        new_response_two.follow()

        new_response_three = self.testapp.post('/new', status=302)
        tally_three_url = new_response_three.headers['Location']
        new_response_three.follow()

        self.assertNotEqual(tally_one_url, tally_two_url)
        self.assertNotEqual(tally_one_url, tally_three_url)
        self.assertNotEqual(tally_two_url, tally_three_url)

if __name__ == '__main__':
    unittest.main()
