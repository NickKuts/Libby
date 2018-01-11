import unittest
import os
import shutil

from api_testing import api_testing


class TestAPI(unittest.TestCase):
    """ Tests for `api_testing.py` """

    """ For testing purposes we'll use another directory """
    api_testing.json_dir = './api_testing/data_files_test/'
    json_dir = api_testing.json_dir

    @classmethod
    def setUpClass(cls):  # pragma: no cover
        """ Remove the dir if it exists to ensure code coverage """
        if os.path.exists(cls.json_dir):
            shutil.rmtree(cls.json_dir)

    def test_file_creation(self):
        """ Test whether the function `do_request_file` creates a file """
        response = api_testing.do_request_file('something')
        self.assertTrue(os.path.exists(self.json_dir))
        self.assertTrue(response['filename'] in os.listdir(self.json_dir))

    def test_file_creation_with_prettyprint(self):
        """ Test whether the function `do_request_file` creates a file with prettyprint """
        response = api_testing.do_request_file('something', pretty_print='1')
        self.assertTrue(os.path.exists(self.json_dir))
        self.assertTrue(response['filename'] in os.listdir(self.json_dir))
        with open(self.json_dir + response['filename']) as f:
            content = list(f)
            self.assertTrue(len(content) > 1)

    def test_file_creation_without_prettyprint(self):
        """ Test whether the function `do_request_file` creates a file without prettyprint """
        response = api_testing.do_request_file('something')
        self.assertTrue(os.path.exists(self.json_dir))
        self.assertTrue(response['filename'] in os.listdir(self.json_dir))
        with open(self.json_dir + response['filename']) as f:
            content = list(f)
            self.assertTrue(len(content) == 1)

    def test_json_dir(self):
        self.assertEqual(self.json_dir, api_testing.json_dir)

    def test_status_code(self):
        """ Test whether the `do_request_json()` returns a 200 response code """
        response = api_testing.do_request_json('')
        self.assertEqual(response['status_code'], 200)

    def test_remove_json(self):
        """ Test whether `remove_json_files()` deletes files """
        api_testing.remove_json_files()
        self.assertTrue(os.listdir(self.json_dir) == [])

    @classmethod
    @unittest.skipIf(os.path.exists(api_testing.json_dir), "test directory does not exist")
    def tearDownClass(cls):  # pragma: no cover
        """ Delete the now non-needed directory """
        shutil.rmtree(cls.json_dir)
