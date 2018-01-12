import unittest
import json
from lambda_func import main_handler
from lambda_func import util


class TestUtil(unittest.TestCase):

    def test_end(self):
        result = util.handle_session_end_request()
        assert (result['dialogAction']['message']['content'] is not None)


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtil)
    unittest.TextTestRunner(verbosity=2).run(suite)
