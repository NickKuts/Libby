import unittest
import random
import os
import json
from lambda_func import location_utils


# Below we use some _os.path_ functions to find JSON files
# Find the path of this file
_file_location = os.path.dirname(os.path.abspath(__file__))
# Combine with the JSON file for sample utterances
_sample_utterances = _file_location + '/../location_sample_utterances.json'
# Combine with the JSON file for locations
_locations = _file_location + '/../locations.json'


class TestLocationUtils(unittest.TestCase):
    """
    This test suite tests the utility functions for our Location intent.
    These functions can be found under the file _location_utils.py_ in the 
    folder _lambda_func_.
    """

    @classmethod
    def setUpClass(cls):
        # Open the sample utterancs JSON file and save the content
        with open(_sample_utterances, 'r') as fp:
            cls.samp_utts = json.load(fp)

    @staticmethod
    def create_rndm_string(length=0):
        """
        This is a helper function for creating random unicode strings for
        our tests below. The strings are of length defined by the similarly
        named parameter.
        :param length the length of the output string
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
        # but first create the response string (in case of failure)
        msg = 'The string "{}" did not get a score of 100, but {}.'
        for i in range(0, ran_len):
            string = self.create_rndm_string(length=str_len)
            result = location_utils.ratio(string, string)
            self.assertTrue(
                result == 100,
                msg.format(string, result))

        # Check if non-exact strings do not equal a score of 100
        # but first create the response string (in case of failure)
        msg = 'The strings (str0: {}) and (str1: {}) got a score of 100, ' \
              'but should have gotten <100.'
        for i in range(0, ran_len):
            str0 = self.create_rndm_string(length=str_len)
            str1 = self.create_rndm_string(length=str_len)
            # Just to be sure, let's check that the string are not equal
            while str0 == str1:  # pragma: no cover
                str0 = self.create_rndm_string(length=str_len)
            result = location_utils.ratio(str0, str1)
            self.assertFalse(
                result == 100,
                msg.format(str0, str1))

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
        These tests do not actually use any assertion functions, but only
        checks if the function runs without errors.
        Note: we only test with type `bytes` here as testing with type `str`
              is implicitly tested in the other tests
        """

        # First we test with both parameters being of type `bytes`
        location_utils.ratio(
            self.create_rndm_string(length=10).encode('utf-8'),
            self.create_rndm_string(length=10).encode('utf-8'))
        # Then with only one parameter being of type `bytes`
        location_utils.ratio(
            self.create_rndm_string(length=10).encode('utf-8'),
            self.create_rndm_string(length=10))
        location_utils.ratio(
            self.create_rndm_string(length=10),
            self.create_rndm_string(length=10).encode('utf-8'))

    def test_parse_trans(self):
        """
        This test checks whether our implementation of the _parse_trans_
        function works as expected.
        """

        # How many iterations of the test we run
        test_amount = 20
        # How long the random string should be
        str_len = 20

        # The regular expression part that will be formatted in below
        reg = '(?P<location>.+)'

        def helper(st):
            """
            A helper function for extracting only those utterances that have
            'place' in them for the filtering below.
            :param st: the string to check
            :return: whether the string should be filtered or not (boolean)
            """
            return not 'place_two' in st and 'place' in st

        # Let's filter the sample utterances and then format them
        samp_utts = list(filter(lambda reg: helper(reg), self.samp_utts))
        samp_utts = list(map(lambda st: st.format(place=reg), samp_utts))

        # Let's test the parser for each sample utterances
        for samp in samp_utts:
            # Now let's give the parser some random strings
            for i in range(0, test_amount):
                # We create a random string to test with, it cannot include the
                # newline character as _re_ does not consider those
                rndm_str = '\n'
                while '\n' in rndm_str:  # pragma: no cover
                    rndm_str = self.create_rndm_string(str_len)
                # We replace the regex part with the random string
                trans = samp.replace(reg, rndm_str)
                # Put through the parser
                result = location_utils.parse_trans(trans, samp_utts)
                # Create a response string in case of failure
                msg = 'The input string "{}" did not yield "{}", but "{}"'
                # And check whether the output of the parser is the string
                self.assertTrue(
                    result == rndm_str,
                    msg.format(trans, rndm_str, result))

    def test_parse_trans_error(self):
        """
        This test checks whether out implementation of the _parse_trans_
        function handles errors correctly.
        """

        # How many iterations of the test we run
        test_amount = 20
        
        # Create some sample utterances that should result in an error
        samp_utts = [
            'where is',
            'nothing'
        ]

        # Let's test the parser for each sample utterance
        for samp in samp_utts:
            for i in range(0, test_amount):
                # Put through the parser
                result = location_utils.parse_trans(samp, samp_utts)
                # Create a response string in case of failure
                msg = 'The input string "{}" did not yield "{}", but "{}"'
                # And check whether the output of the parser is the string
                self.assertTrue(
                    result == samp,
                    msg.format(samp, samp, result))

    def test_parse_trans_two(self):
        """
        This test checks whether our implementation of the _parse_trans_two_
        function works as expected.
        """

        # How many iterations should be done in the test
        test_amount = 20
        # The regex patterns used in all sample utterances
        reg1 = '(?P<location>.+)'
        reg2 = '(?P<location_two>.+)'

        # Get all the sample utterances that we have
        # (the ones with two locations to be found)
        samp_utts = []
        for samp in self.samp_utts:
            if 'place_two' in samp and '{place} {place_two}' != samp:
                samp_utts.append(samp)
        samp_utts = list(map(lambda st: st.format(place=reg1, place_two=reg2), samp_utts))

        # Let's teset the parser for each sample utterances
        for samp in samp_utts:
            # Now let's give the parser some random strings
            for i in range(0, test_amount):
                # We create some random strings to test with, it cannot include 
                # the newline character as _re_ does not consider these
                rndm_str1 = '\n'
                while '\n' in rndm_str1:  # pragma: no cover
                    rndm_str1 = self.create_rndm_string(10)
                rndm_str2 = '\n'
                while '\n' in rndm_str2:  # pramga: no cover
                    rndm_str2 = self.create_rndm_string(10)
                # Save the strings as tuples
                ans = (rndm_str1, rndm_str2)
                # We replace the regex parts with random strings
                trans = samp.replace(reg1, rndm_str1).replace(reg2, rndm_str2)
                # Put through the parser
                result = location_utils.parse_trans_two(trans, samp_utts)
                # Create the response string in case of failure
                msg = 'The input string "{}" did not yield "{}", but "{}"'
                print('trans: {}\nsampl: {}\nres: {}\n'.format((trans,), samp, result))
                # And check whether the output of the parser is the string tuple
                self.assertTrue(
                    ans == result,
                    msg.format(trans, ans, result))

    def test_parse_trans_two_error(self):
        """
        This test checks whether the function _parse_trans_two_ handles
        errors correctly.
        """

        # How many iterations of the test we run
        test_amount = 20

        # Create some sample utterances that should result in an error
        samp_utts = [
            'how do get from somewhere to anotherwhere',
            'this should fail <location_two>'
        ]

        # Let's test  the parser for each sample utterance
        for samp in samp_utts:
            for i in range(0, test_amount):
                # Put through the parser
                result = location_utils.parse_trans_two(samp, samp_utts)
                # Create a response string in case of failure
                msg = 'The input string "{}" did not yield "{}", but "{}"'
                # Create the tuple that should be the response
                ans = (samp, samp)
                # And check whether the output of the parser is a tuple of the input
                self.assertTrue(
                    result == ans,
                    msg.format(samp, ans, result))

    def test_parse_opening_hours(self):
        """
        This test checks whether the whether the function _parse_opening_hours_ 
        works as expected.
        """
        
        # Array for all opening hours
        hours = []

        # Get all locations' opening hours
        with open(_locations, 'r') as fp:
            locs = json.load(fp)
            for _, data in locs.items():
                hs = data.get('opening_hours', None)
                if hs:
                    hours.append(hs)

        # Error message
        msg = '"{}" did not yield a valid string'
        
        # We simply check that we are returned a string of length > 0
        for hour in hours:
            res = location_utils.parse_opening_hours(hour)
            self.assertTrue(
                len(res) > 0, 
                msg.format(hour))

