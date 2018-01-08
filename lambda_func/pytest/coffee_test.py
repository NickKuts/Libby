import unittest
import sys
sys.path.append("..")

from lambda_func import main_handler
import json
import sys
sys.path.append("..")


class TestUtilDate(unittest.TestCase):

    test_data = json.load(open("./lambda_func/pytest/coffee_test.json"))
    json_data = json.load(open("./lambda_func/pytest/robertscoffee.json"))
    testGroups = [
        ['morning latte', 'flat white'],
        ['classics', 'tea', 'chococino', 'espresso', 'con panna', 'ice latte', 'ice mocha', 'ice tea', 'italian soda'],
        ['oriental latte', 'cocoa', 'coffee', 'cappucinos', 'cold coffee drinks'],
        ['classics', 'cappucinos', 'cold coffee drinks'],
        ['coffee', 'tea', 'morning latte', 'oriental latte', 'flat white', 'chococino', 'espresso', 'con panna',
         'cocoa', 'ice latte', 'ice mocha', 'ice tea', 'italian soda']]
    '''
    def testLatte(self):
        event = self.test_data['coffee drinks']
        result = main_handler.lambda_handler(event, None)
        print("result", result)
        assert (result != None)
    '''

    def testDrinks(self):
        print("----------DRINKS----------")
        final_map = {}  # dict#map(lambda x: x.value, dict)
        for i in self.json_data.values():
            final_map.update(i)

        for name in final_map:
            print("name", name)
            event = self.test_data[name]
            # print("data", event)
            # print(event['name'])
            result = main_handler.lambda_handler(event, None)
            print("result", result['response']['outputSpeech']['text'])
            assert (result is not None)
        print("number of drinks tested: " + str(len(final_map)))

    def testCategories(self):
        print("----------CATEGORIES----------")
        # for group in self.testGroups:
        for category in self.json_data:
            print("name", category)
            event = self.test_data[category]
            # print("data", event)
            # print(event['name'])
            result = main_handler.lambda_handler(event, None)
            print("result", result['response']['outputSpeech']['text'])
            assert (result is not None)
        print("number of categories tested: " + str(len(self.json_data)))


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilDate)
    unittest.TextTestRunner(verbosity=2).run(suite)
