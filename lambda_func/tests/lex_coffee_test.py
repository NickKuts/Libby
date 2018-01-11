import unittest
import sys

sys.path.append("..")
import main_handler


class TestUtilDate(unittest.TestCase):
    event = {
        "currentIntent": {
            "name": "Get_Drinks",
            "slots": {
                "category": "classics"
            }
        }
    }
    result = main_handler.lambda_handler(event, None)
    print("result", result)
    assert (result is not None)

    event = {
        "currentIntent": {
            "name": "Get_Prices",
            "slots": {
                "consumable": "coffee"
            }
        }
    }
    result = main_handler.lambda_handler(event, None)
    print("result", result)
    assert (result is not None)


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilDate)
    unittest.TextTestRunner(verbosity=2).run(suite)
