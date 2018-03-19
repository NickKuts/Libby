import unittest
#from lambda_func import main_handler, location
from lambda_func import location
import json
import os


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

    def test_address(self):
        """ 
        This test checks wether the intent is able to find addresses for all
        locations, if they have one
        """

        # Get the right test input
        all_locs_data = self.test_data.get('all_locs', {})
        # Create inputTranscript for this test
        input_transcript = 'What is the address of {}'

        # Saving the formattable strings from the input
        new_place = all_locs_data['currentIntent']['slots']['place']
        new_inp_tr = all_locs_data['inputTranscript']
        
        def update_input(place, input_trans):
            """
            Helper function to update the value of the all_locs input.
            param: place value of place in the slot of the input
            param: input_trans value of the inputTranscript of the input
            """
            # Update slot value
            all_locs_data['currentIntent']['slots']['place'] = new_place.format(place)
            # Update inputTranscript
            all_locs_data['inputTranscript'] = new_inp_tr.format(input_trans)

        for loc, data in self.locations.items():
            aliases = data.get('aliases', [])
            # Extract the address from the data and set to lowercase
            addr = data['address']
            if not addr:
                addr = 'sorry'
            addr = addr.lower()
            for alias in aliases:
                trans = input_transcript.format(alias)
                update_input(alias, trans)
                result = location.location_handler(all_locs_data)
                # Set the result to lower for easier checking
                result = self.extract_response(result).lower()
                # Check wether the actual address is found in the response 
                self.assertTrue(
                    addr in result, 
                    'The address of {} ({}) is "{}", but got response "{}".'.format(
                        alias, loc, addr, result))


def main():
    pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLocation)
    unittest.TextTestResult(verbosity=2).run(suite)

