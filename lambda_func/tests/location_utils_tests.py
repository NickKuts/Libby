import unittest
from lambda_func import location_utils
import json
import os
import random
import string


class TestLocationUtils(unittest.TestCase):
    """
    This test suite tests the utility functions for our Location intent.
    """

    def create_rndm_string(self, length=0):
        """
        This is a helper function for creating random unicode strings for
        our tests below. The strings are of length defined by the similarly
        named parameter.
        param: length the length of the output string
        """
        return ''.join([chr(random.randint(0, 256)) for _ in range(0, length)])

    def test_ratio_ratios(self):
        """
        This test checks whether the _ratio_ function returns expected values
        for certain string, e.g. `100` for equal strings and `0` for totally
        differing strings.
        """

        # Variables for defining ranges and string length
        ran_len = 100
        str_len = 30
        
        # Check if exactly equal strings equal a score of 100
        for i in range(1, ran_len):
            string = self.create_rndm_string(length=str_len)
            result = location_utils.ratio(string, string)
            self.assertTrue(
                result == 100,
                'The string "{}" did not get a score of 100, but {}'
                    .format(string, result))

        # Check if non-exact strings do not equal a score of 100
        for i in range(1, ran_len):
            str0 = self.create_rndm_string(length=str_len)
            str1 = self.create_rndm_string(length=str_len)
            # Just to be sure, let's check that the string are not equal
            while str0 == str1:
                str0 = self.create_rndm_string(length=str_len)
            result = location_utils.ratio(str0, str1)
            self.assertFalse(
                result == 100,
                'The strings (str0: {}) and (str1: {}) got a score of 100, '
                'but should have gotten <100.'
                    .format(str0, str1))

    def test_ratio_return_0(self):
        """
        This test checks whether the _ratio_ function in location_utils returns
        0 for correct outputs. This occurs when at least one of the strings are
        either `None` or of length 0.
        """

        # First we test with both values being `None`
        result = location_utils.ratio(None, None)
        self.assertTrue(
            result == 0,
            'Parameters being None should result in score of 0 from ratio.')

        # Then we test if only one is None
        result = location_utils.ratio(None, self.create_rndm_string(length=10))
        self.assertTrue(
            result == 0,
            'A parameter being None should result in a score of 0 from ratio')
        result = location_utils.ratio(self.create_rndm_string(length=10), None)
        self.assertTrue(
            result == 0,
            'A parameter being None should result in a score of 0 from ratio')

        # Do the same as above, but with strings of length 0 instead of None
        result = location_utils.ratio('', '')
        self.assertTrue(
            result == 0,
            'Parameters being strings with length 0 should result in a '
            'score of 0 from ratio')

        result = location_utils.ratio('', self.create_rndm_string(length=10))
        self.assertTrue(
            result == 0,
            'A string with length 0 should result in a score of 0 from ratio')
        result = location_utils.ratio(self.create_rndm_string(length=10), '')
        self.assertTrue(
            result == 0,
            'A string with length 0 should result in a score of 0 from ratio')

    def test_ratio_encoding(self):
        """
        This test checks whether the inputs for the _ratio_ function are 
        properly decoded (if they are of type `bytes`).
        Note: we only test with type `bytes` here as testing with type `str`
              is implicitly tested in the other tests
        """

        # First we test with both parameters being of type `bytes`
        result = location_utils.ratio(
                self.create_rndm_string(length=10).encode('utf-8'),
                self.create_rndm_string(length=10).encode('utf-8'))
        # Then with only one parameter being of type `bytes`
        result = location_utils.ratio(
                self.create_rndm_string(length=10).encode('utf-8'),
                self.create_rndm_string(length=10))
        result = location_utils.ratio(
                self.create_rndm_string(length=10),
                self.create_rndm_string(length=10).encode('utf-8'))

