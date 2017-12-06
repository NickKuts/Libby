import unittest
import os

# import main_handler
from api_testing import main_handler
from api_testing import api_testing
import json


class TestUtilDate(unittest.TestCase):
    """ Tests for `api_testing.py` """

    json_dir = '../' + api_testing.json_dir

    def setUp(self):
        pass

    def tearDown(self):
        """ Remove all created JSON test files """
        for f in os.listdir(self.json_dir):
            os.remove(os.path.join(self.json_dir, f))

    def test_status_code(self):
        """ Test wether the `do_requeset_json()` returns a 200 response code """
        response = api_testing.do_request_json('')
        self.assertEqual(response['status_code'], 200)

    def test_file_creation(self):
        """ Test wether the function `do_request_file` creates a file """
        response = api_testing.do_request_file('something')
        self.assertTrue(response['filename'] in os.listdir(self.json_dir))
