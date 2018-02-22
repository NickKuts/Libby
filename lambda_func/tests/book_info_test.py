import unittest
import json
import requests
from lambda_func import main_handler, book_info


class TestBookInfo(unittest.TestCase):
    test_data = json.load(open("tests/book_info_test.json"))
    headers = {'Accept': 'application/json'}

    def test_book_info(self):
        books = ['findComputer']
        for i in books:
            test_input = self.test_data[i]
            result = main_handler.lambda_handler(test_input, None)
            print("result: " + str(result))

            sess = requests.Session()
            sess.headers.update(self.headers)
            right_result = sess.request(url=test_input['url'],
                                             method='GET').json()
            sess.close()
            # print("OOOOO: " + str(right_result))
            assert (result == book_info.parse_subject(right_result,
                                                      test_input['subject']))


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBookInfo)
    unittest.TextTestRunner(verbosity=2).run(suite)
