import unittest

import sys
sys.path.append("..")

#import main_handler
import main_handler
#from lambda_func import main_handler
import json

class TestUtilDate(unittest.TestCase):
        
    def setUp(self):
        #init_something()
        pass
        
    def tearDown(self):
        #teardown_something()
        pass
        
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())

    def test_weather(self):
        self.assertEqual('foo', 'foo')
        json_data = json.load(open("weather_test.json"))
        result = main_handler.lambda_handler(json_data, None)
        print("result", result)
        assert(result != None)


def main():
    print("Main function")
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilDate)
    unittest.TextTestRunner(verbosity=2).run(suite)
