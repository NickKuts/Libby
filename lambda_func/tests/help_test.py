import unittest
from lambda_func import main_handler
import json


class TestHelp(unittest.TestCase):
    test_data = json.load(open("./tests/help_test.json"))

    def test_basic_help(self):
        event = ['basic', 'help_roberts_coffee', 'help_weather',
                 'help_location','need_help_location', 'help_books',
                 'help_author', 'help_random']
        for i in event:
            test_str = self.test_data[i]
            result = main_handler.lambda_handler(test_str, None)
            print("result", result)
            assert (result is not None)


def main():  # pragma: no cover
    print("Main function")


if __name__ == '__main__':  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHelp)
    unittest.TextTestRunner(verbosity=2).run(suite)
