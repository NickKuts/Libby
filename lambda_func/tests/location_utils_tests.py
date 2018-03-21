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

    def create_rndm_string(
            self, 
            upp_chars=string.ascii_uppercase, 
            low_chars=string.ascii_lowercase, 
            digs=string.digits, 
            length=0):
        """
        This is a helper function for our tests. It creates a random string
        of length `am` consisting of characters (upper and lower case) and 
        digits depending on the value of the corresponding parameters above
        param: upper_chars boolean if uppercase characters should be added
        param: low_chars boolean if lowercase characters should be added
        param: digs boolean if digits should be added
        param: m the length of the output string
        """
        all_chars = upp_chars + low_chars + digs
        return ''.join(random.choices(all_chars, k=length))

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

    def test_ratio_formats(self):
        """
        This test checks whether the _ratio_ function actually convert strings
        of differing types correctly. The function can receive strings of type
        `str` and `unicode`, and in case they differ they should be converted 
        to `unicode`, and if any of them are `None`, the function should 
        return 0.
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

