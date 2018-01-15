import unittest
from lambda_func import main_handler
import json
#import main_handler


class TestUtilHelp(unittest.TestCase):
    test_data = json.load(open("./tests/help_test.json"))

    def test_basic_help(self):
        event = self.test_data['basic']
        result = main_handler.lambda_handler(event, None)
        print("result", result)
        assert (result is not None)

    def test_robertscoffee_help(self):
        event = self.test_data['roberts coffee']
        result = main_handler.lambda_handler(event, None)
        print("result", result)
        assert (result is not None)

    """def test_weather_help(self):
        event = self.test_data['weather']
        result = main_handler.lambda_handler(event, None)
        print("result", result)
        assert (result is not None)"""


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilHelp)
    unittest.TextTestRunner(verbosity=2).run(suite)
