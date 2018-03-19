import unittest
from lambda_func import main_handler
import json
import os


# Find the path of this file
_file_location = os.path.dirname(os.path.abspath(__file__))
# Combine with the JSON file for locations
_locations_file = _file_location + '../locations.json'


class TestLocation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Open the locations JSON file and save the content
        with open(_locations_file, 'r') as fp:
            cls.locations = json.load(fp)


def main():
    pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLocation)
    unittest.TextTestResult(verbosity=2).run(suite)

