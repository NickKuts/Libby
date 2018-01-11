import unittest
import os

from api_testing import api_testing


class TestAPI(unittest.TestCase):
    """ Tests for `api_testing.py` """

    json_dir = api_testing.json_dir

    def setUp(self):
        if not os.path.exists(self.json_dir):
            os.makedirs(self.json_dir)

    def tearDown(self):
        """ Ensure that all .json files gets deleted """
        for f in os.listdir(self.json_dir):
            if f.endswith('.json'):
                os.remove(os.path.join(self.json_dir, f))

    def test_json_dir(self):
        self.assertEqual(self.json_dir, api_testing.json_dir)

    def test_status_code(self):
        """ Test whether the `do_request_json()` returns a 200 response code """
        response = api_testing.do_request_json('')
        self.assertEqual(response['status_code'], 200)

    def test_file_creation(self):
        """ Test whether the function `do_request_file` creates a file """
        response = api_testing.do_request_file('something')
        self.assertTrue(response['filename'] in os.listdir(self.json_dir))

    def test_remove_json(self):
        """ Test whether `remove_json_files()` deletes files """
        api_testing.remove_json_files()
        for f in os.listdir(self.json_dir):
            self.assertFalse(f.endswith('.json'))
