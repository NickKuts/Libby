import unittest
import os
import sys
sys.path.append('..')

# import main_handler
from api_testing import main_handler
from api_testing import api_testing


class TestAPI(unittest.TestCase):
    """ Tests for `api_testing.py` """

    json_dir = '../' + api_testing.json_dir

    def setUp(self):
        pass

    def tearDown(self):
        """ Remove all created JSON test files """
        for f in os.listdir(self.json_dir):
            os.remove(os.path.join(self.json_dir, f))

    def test_status_code(self):
        """ Test whether the `do_request_json()` returns a 200 response code """
        response = api_testing.do_request_json('')
        self.assertEqual(response['status_code'], 200)

    def test_file_creation(self):
        """ Test whether the function `do_request_file` creates a file """
        response = api_testing.do_request_file('something')
        self.assertTrue(response['filename'] in os.listdir(self.json_dir))


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
