import unittest
from lambda_func import location
import json
import os
import random
import string


# Find the path of this file
_file_location = os.path.dirname(os.path.abspath(__file__))
# Combine with the JSON file for locations
_locations_file = _file_location + '/../locations.json'
# Combine with the JSON file for intents
_test_data = _file_location + '/location_test.json'


class TestLocation(unittest.TestCase):
    """ This test suite tests our location intent. """

    @classmethod
    def setUpClass(cls):
        # Open the locations JSON file and save the content
        with open(_locations_file, 'r') as fp:
            cls.locations = json.load(fp)
        with open(_test_data, 'r') as fp:
            cls.test_data = json.load(fp)

    def extract_response(self, res):
        return res['dialogAction']['message']['content']

    def update_input(self, data, place, input_trans):
        """
        Helper function to update value of the 'data' input, which simulates
        the input to the location intent.
        param: data the input to be updated
        param: place value of place in the slot of the input
        param: input_trans value of the inputTranscript of the input
        """
        if place:  # Update place if place is not None
            data['currentIntent']['slots']['place'] = place
        if input_trans:  # Update inputTranscript if input_trans is not None
            data['inputTranscript'] = input_trans

    def test_address(self):
        """ 
        This test checks whether the intent is able to find addresses for all
        locations, if they have one
        """

        # Get the right test input
        all_locs_data = self.test_data.get('all_locs', {})
        # Create inputTranscript for this test
        input_transcript = 'What is the address of {}'

        # Saving the formattable strings from the input
        new_place = all_locs_data['currentIntent']['slots']['place']
        new_inp_tr = all_locs_data['inputTranscript']

        for loc, data in self.locations.items():
            aliases = data.get('aliases', [])
            # Extract the address from the data and set to lowercase
            addr = data['address']
            if not addr:  # If the location does not have an address the intent
                addr = 'sorry'  # returns a string including 'sorry'
            addr = addr.lower()
            for alias in aliases:
                # Update the input for the intent
                trans = input_transcript.format(alias)
                self.update_input(
                    all_locs_data, 
                    new_place.format(alias), 
                    new_inp_tr.format(trans)
                )
                result = location.location_handler(all_locs_data)
                # Set the result to lower for easier checking
                result = self.extract_response(result).lower()
                # Check whether the actual address is found in the response 
                self.assertTrue(
                    addr in result, 
                    'The address of {} ({}) is "{}", but got response "{}".'
                        .format(alias, loc, addr, result))

        # After the test, sanitize the input data
        all_locs_data['currentIntent']['slots']['place'] = '{}'
        all_locs_data['inputTranscript'] = '{}'

    def test_hours(self):
        """
        This test checks whether all places that have opening hours are 
        represented by the hour that we know of.
        """

        # Get the right test input
        all_locs_data = self.test_data.get('all_locs', {})
        # Create inputTranscript for this test
        input_transcript = 'opening hours of {}'

        # Saving formattable strings from the input
        new_place = all_locs_data['currentIntent']['slots']['place']
        new_inp_tr = all_locs_data['inputTranscript']

        for loc, data in self.locations.items():
            # Extract the address from the data and set to lowercase
            hours = data.get('opening_hours', None)
            if not hours:  # Same as above, a string with 'sorry' is returned
                hours = 'sorry'  # if no hours exist
            hours = hours.lower()
            # Update the input for the intent
            trans = input_transcript.format(loc)
            self.update_input(
                all_locs_data,
                new_place.format(loc),
                new_inp_tr.format(trans)
            )
            result = location.location_handler(all_locs_data)
            # Set the result to lower for easier checking
            result = self.extract_response(result).lower()
            # Check whether the response is correct
            self.assertTrue(
                hours in result,
                'The opening hours of {} is "{}", but got response "{}"\n\n{}.'
                    .format(loc, hours, result, all_locs_data))

        # After the test, sanitize the input data
        all_locs_data['currentIntent']['slots']['place'] = '{}'
        all_locs_data['inputTranscript'] = '{}'

    def test_no_ans(self):
        """
        This test checks whether the intent returns a correct response in case
        it gets a location it has no idea of.
        """

        # Get the right test input
        all_locs_data = self.test_data.get('all_locs', {})
        # Create inputTranscript
        input_transcript = 'What is the address of {}'

        # Saving formattable string from inputTranscript
        new_inp_tr = all_locs_data['inputTranscript']

        # Let's give the intent some real location that it should 
        # have no data about
        locs = ['hamburg', 'shanghai', 'tokyo', 'australia']
        for loc in locs:
            # Update the input for the intent
            trans = input_transcript.format(loc)
            self.update_input(
                all_locs_data,
                None,
                new_inp_tr.format(trans)
            )
            result = location.location_handler(all_locs_data)
            # Check whether the response does NOT contain the location
            self.assertFalse(
                loc in result,
                'The Location intent should not have found an address for: {}'
                    .format(loc))

        # Now, let's test with some random gibberish
        for i in range(0, 20):
            # Create a random string consisting of random chars and nums
            rndm_str = ''.join(
                    random.choices(string.ascii_uppercase + string.digits, k=20))
            # Update the input for the intent
            trans = input_transcript.format(rndm_str)
            self.update_input(
                all_locs_data,
                None,
                new_inp_tr.format(trans)
            )
            result = location.location_handler(all_locs_data)
            # Check whether the response does NOT contain the location
            self.assertFalse(
                rndm_str in result,
                'The Location intent should not have found an address for: {}'
                    .format(rndm_str))

def main():  # pragma: no cover
    pass


if __name__ == '__main__':  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLocation)
    unittest.TextTestResult(verbosity=2).run(suite)

