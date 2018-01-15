import unittest

from lambda_func import main_handler
import json


class TestUtilDate(unittest.TestCase):

    def setUp(self):
        # init_something()
        pass

    def tearDown(self):
        # teardown_something()
        pass

    def test_weather(self):
        self.assertEqual('foo', 'foo')
        json_data = json.load(open("./tests/weather_test.json"))
        # result = main_handler.lambda_handler(json_data, None)
        # assert(result != None)
        pass

def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilDate)
    unittest.TextTestRunner(verbosity=2).run(suite)
