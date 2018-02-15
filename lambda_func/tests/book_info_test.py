import unittest
import json
from lambda_func import main_handler, book_info

test_data = json.load(open("./tests/help_test.json"))


class TestBookInfo(unittest.TestCase):
    test_data = json.load(open("tests/book_info_test.json"))

    def test_book_info(self):
        books = ['findComputer']
        for i in books:
            test_input = self.test_data[i]
            result = main_handler.lambda_handler(test_input, None)
            print("result", result)
            assert (result == test_input['right_result'])


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBookInfo)
    unittest.TextTestRunner(verbosity=2).run(suite)
