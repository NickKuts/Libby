import unittest
from lambda_func import main_handler
import json


class TestUtilHelp(unittest.TestCase):
    test_data = json.load(open("./tests/help_test.json"))

    def test_basic_help(self):
        event = ['basic', 'help_roberts_coffee', 'help_weather',
                 'help_location']
        for i in event:
            testStr = self.test_data[i]
            result = main_handler.lambda_handler(testStr, None)
            print("result", result)
            assert (result is not None)


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilHelp)
    unittest.TextTestRunner(verbosity=2).run(suite)
