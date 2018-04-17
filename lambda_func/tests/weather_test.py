import unittest

from lambda_func import main_handler
import json


class TestUtilDate(unittest.TestCase):

    def test_weather(self):
        json_data = json.load(open("./tests/weather_test.json"))
        result = main_handler.lambda_handler(json_data, None)
        assert(result is not None)


def main():  # pragma: no cover
    print("Main function")


if __name__ == '__main__':  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilDate)
    unittest.TextTestRunner(verbosity=2).run(suite)
