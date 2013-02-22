from webtest import TestApp
import unittest

import tally.server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.testapp = TestApp(tally.server.app)

    def test_index(self):
        self.assertEqual(self.testapp.get('/').status, '200 OK')

    def test_can_create_new_tally_from_index(self):
        index_response = self.testapp.get('/')
        self.assertTrue('action="new"' in index_response)
        self.assertTrue('<button type="submit"' in index_response)

    def test_404_from_unknown_key(self):
        self.testapp.get('/dartmoor', status=404)

    def test_new_key(self):
        new_response = self.testapp.post('/new', status=302)
        self.assertTrue('Location' in new_response.headers)
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

    normal_form = {'name': 'Days in prison',
                'desc': 'The number of days behind bars.',
                'init': '451',
                'unit': 'prison days',
                'inc': ['-41', '+42']}

    def post_new_tally_with_data(self, form):
        new_response = self.testapp.post('/new', form, status=302)
        return new_response.follow()

    def test_new_tally_with_name(self):
        tally_response = self.post_new_tally_with_data(self.normal_form)
        self.assertTrue('Days in prison' in tally_response)

    def test_new_tally_with_desc(self):
        tally_response = self.post_new_tally_with_data(self.normal_form)
        self.assertTrue('The number of days behind bars.' in tally_response)

    def test_new_tally_with_init(self):
        tally_response = self.post_new_tally_with_data(self.normal_form)
        self.assertTrue('451' in tally_response)

    def test_new_tally_with_unit(self):
        tally_response = self.post_new_tally_with_data(self.normal_form)
        self.assertTrue('prison days' in tally_response)

    def test_new_tally_with_inc(self):
        tally_response = self.post_new_tally_with_data(self.normal_form)
        self.assertTrue('-1' in tally_response)
        self.assertTrue('+1' in tally_response)


if __name__ == '__main__':
    unittest.main()
