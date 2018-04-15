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
            # print("=========" + test + "========")
            test_input = self.test_data[test]
            is_author = test_input["is_author"]
            result = main_handler.lambda_handler(test_input, None)

            sess = requests.Session()
            sess.headers.update(self.headers)

            right_result = sess.request(url=test_input['url'],
                                        method='GET').json()
            sess.close()

            subject = test_input.get('subject', 'default subject')
            author = test_input.get('author')
            if is_author:
                assert(result == book_info.parse_author(right_result,
                                                        {'author': author}))
            else:
                assert (result == book_info.parse_subject(right_result, subject,
                                                          {'author': author}))


def main():  # pragma: no cover
    print("Main function")


if __name__ == '__main__':  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBookInfo)
    unittest.TextTestRunner(verbosity=2).run(suite)
