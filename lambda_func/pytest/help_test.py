import unittest
from lambda_func import main_handler
import json
#import main_handler

class TestUtilDate(unittest.TestCase):

    def basic_help_test(self):
        event = self.test_data['basic']
        result = main_handler.lambda_handler(event, None)
        print("result", result)
        assert (result != None)

        print("number of helps tested: " + str(len(self.json_data)))


""" def test_help(self):
        print("____help___")
        final_map = {}
        for help in self.test_data[help]
        
        print("----------DRINKS----------")
        final_map = {}  # dict#map(lambda x: x.value, dict)
        for i in self.json_data.values():
            final_map.update(i)

        for category in self.json_data:
        print("name", category)
        event = self.test_data[category]
        # print("data", event)
        # print(event['name'])
        result = main_handler.lambda_handler(event, None)
        print("result", result['response']['outputSpeech']['text'])
        assert (result is not None)"""

        #print("number of helps tested: " + str(len(self.json_data)))


def main():
    print("Main function")


if __name__ == '__main__':
    pass