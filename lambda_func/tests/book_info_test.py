import unittest
import json
from lambda_func import main_handler, book_info


class TestRoberts(unittest.TestCase):
    test_data = json.load(open("tests/book_info_test.json"))


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoberts)
    unittest.TextTestRunner(verbosity=2).run(suite)
