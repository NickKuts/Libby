import unittest
import json
import requests
from lambda_func import main_handler, book_info


class TestBookInfo(unittest.TestCase):
    test_data = json.load(open("tests/book_info_test.json"))
    headers = {'Accept': 'application/json'}

    def test_book_info(self):
        tests = []
        for name in self.test_data:
            tests.append(name)
        for test in tests:

            print("test:", test)
            test_input = self.test_data[test]
            result = main_handler.lambda_handler(test_input, None)
            # print("result: " + str(result))

            sess = requests.Session()
            sess.headers.update(self.headers)
            right_result = sess.request(url=test_input['url'],
                                        method='GET').json()
            sess.close()
            # print("result: " + str(result))
            # print("right result: " + str(right_result))
            # assert(1 == 2)
            author = test_input.get('author')
            subject = test_input.get('subject', 'default subject')
            assert (result == book_info.parse_subject(right_result,
                                                      subject,
                                                      author))




def main():  # pragma: no cover
    print("Main function")


if __name__ == '__main__':  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBookInfo)
    unittest.TextTestRunner(verbosity=2).run(suite)
