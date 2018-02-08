import unittest
import json
from lambda_func import main_handler, robertscoffee


class TestRoberts(unittest.TestCase):
    test_data = json.load(open("tests/lex_coffee_test.json"))
    json_data = json.load(open("./robertscoffee.json"))

    def test_intro(self):
        result = main_handler.lambda_handler(self.test_data["category"], None)
        print("result", result['dialogAction']['message']['content'])
        assert (result == robertscoffee.intro())
        assert (result['dialogAction']['message']['content'] is not None)

    def test_drinks(self):
        print("----------DRINKS----------")
        final_map = {}
        for i in self.json_data.values():
            final_map.update(i)

        for name in final_map:
            print("name", name)
            event = self.test_data[name]
            # print("data", event)
            # print(event['name'])
            result = main_handler.lambda_handler(event, None)
            print("result", result['dialogAction']['message']['content'])
            assert (result == robertscoffee.prices(event['currentIntent']))
            assert (result['dialogAction']['message']['content'] is not None)
        print("number of drinks tested: " + str(len(final_map)))

    def test_categories(self):
        print("----------CATEGORIES----------")
        for category in self.json_data:
            # print("name", category)
            event = self.test_data[category]
            # print("data", event)
            # print(event['name'])
            result = main_handler.lambda_handler(event, None)
            should = robertscoffee.drinks(event['currentIntent']['slots']['category'])
            print("result", result['dialogAction']['message']['content'])
            print("should", should['dialogAction']['message']['content'])
            assert (result == should)
            assert (result['dialogAction']['message']['content'] is not None)
        print("number of categories tested: " + str(len(self.json_data)))


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoberts)
    unittest.TextTestRunner(verbosity=2).run(suite)
