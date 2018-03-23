import unittest
import json
import os
import random
import string
from lambda_func import location


# Below we use some _os.path_ functions to find JSON files
# Find the path of this file
_file_location = os.path.dirname(os.path.abspath(__file__))
# Combine with the JSON file for locations
_locations_file = _file_location + '/../locations.json'
# Combine with the JSON file for intents
_test_data = _file_location + '/location_test.json'


class TestLocation(unittest.TestCase):
    """ 
    This test suite tests our location intent. 
    The intent itself can be found in the file _location.py_ under the folder
    _lambda_func_.
    """

    @classmethod
    def setUpClass(cls):
        # Open the locations JSON file and save the content
        with open(_locations_file, 'r') as fp:
            cls.locations = json.load(fp)
        with open(_test_data, 'r') as fp:
            cls.test_data = json.load(fp)

    @staticmethod
    def extract_response(res):
        """
        Helper function for extracting a response from the resulting JSON from
        the intent.
        :param res: the JSON formatted response
        :return: the content of the response
        """
        return res['dialogAction']['message']['content']

    @staticmethod
    def update_input(data, place, input_trans):
        """
        Helper function to update value of the 'data' input, which simulates
        the input to the location intent.
        :param data: the input to be updated
        :param place: value of place in the slot of the input
        :param input_trans: value of the inputTranscript of the input
        """
        data['currentIntent']['slots']['place'] = place
        if input_trans:  # inputTranscript should always be something
            data['inputTranscript'] = input_trans

    @staticmethod
    def sanitize_input_data(data):
        """
        A helper function for sanitizing inputs after each test, so that all
        tests have a clean plate
        :param data: input data to be sanitized
        """
        data['currentIntent']['slots']['place'] = '{}'
        data['inputTranscript'] = '{}'

    @staticmethod
    def input_values_to_location(event, input_trans, value1, value2):
        event['currentIntent']['slots']['place'] = value2
        event['currentIntent']['slots']['place_two'] = value1
        event['currentIntent']['slotDetails']['place']['originalValue'] = value2
        event['currentIntent']['slotDetails']['place_two']['originalValue'] = value1
        event['inputTranscript'] = input_trans
        return event

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
                # Create formattable response string
                msg = 'The address of {} ({}) is "{}", but go the response "{}".'
                # Check whether the actual address is found in the response 
                self.assertTrue(
                    addr in result, 
                    msg.format(alias, loc, addr, result))

        # After the test, sanitize the input data
        self.sanitize_input_data(all_locs_data)

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
            # Create response message in case of fail
            msg = 'The opening hours of {} is "{}", got response "{}".'
            # Check whether the response is correct
            self.assertTrue(
                hours in result,
                msg.format(loc, hours, result))

        # After the test, sanitize the input data
        self.sanitize_input_data(all_locs_data)

    def none_existence(self, place):
        """
        This function is a helper function to avoid boiler-plate for other 
        tests.
        We want to  test both the parser and the slot picking mechanisms of the
        intent. The param place defines whether the place (slot) should be 
        named or not, it should be a boolean, True for named, False for not.
        :param place name (if any) of the place slot
        """

        # Get the right test input
        all_locs_data = self.test_data.get('all_locs', {})

        # We want to test all intent functions, so we use this simple for-loop
        # over a list to check each function
        input_transcripts = [
            'What is the address of {}',
            'opening hours of {}',
            'where is {}',
            'location of {}',
        ]

        for input_transcript in input_transcripts:
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
                    None if place else loc,
                    new_inp_tr.format(trans)
                )
                result = location.location_handler(all_locs_data)
                # Create response message in case of fail
                msg = 'The Location intent should not have found an address for: {}'
                # Check whether the response does NOT contain the location
                self.assertFalse(
                    loc in result,
                    msg.format(loc))
    
            # Now, let's test with some random gibberish
            for i in range(0, 20):
                # Create a random string consisting of random chars and nums
                rndm_str = ''.join(  # The string will be of length 20
                        random.choices(string.ascii_uppercase + string.digits, k=20)
                )
                # Update the input for the intent
                trans = input_transcript.format(rndm_str)
                self.update_input(
                    all_locs_data,
                    None,
                    new_inp_tr.format(trans)
                )
                result = location.location_handler(all_locs_data)
                # Create response message in case of fail
                msg = 'The Location intent should not have found an address for: {}'
                # Check whether the response does NOT contain the location
                self.assertFalse(
                    rndm_str in result,
                    msg.format(rndm_str))

            # After each iteration of the outer loop, sanitize input data
            self.sanitize_input_data(all_locs_data)
        # And after the test, sanitize inputs again
        self.sanitize_input_data(all_locs_data)

    def test_ans_slot(self):
        """
        Test the intent when it utilizes the slot value from the input data.
        """
        self.none_existence(False)

    def test_ans_parser(self):
        """
        Test the intent when it utilizes the inputTranscript from the
        inputTranscript
        """
        self.none_existence(True)

    def test_return_fail(self):
        """
        Test for checking whether the intent returns a 'fail' response if the
        inputTranscript only consists of the name (or the inputTranscript is
        not recognized)
        """
        
        # Get the right test input
        all_locs_data = self.test_data.get('all_locs', {})
        # Create inputTranscript's for the test
        input_transes = [
            '{}',
            'something something {}',
        ]

        for loc, data in self.locations.items():
            # Create the inputTranscripts and check them
            for trans in input_transes:
                trans = trans.format(loc).lower()
                self.update_input(
                    all_locs_data,
                    None,
                    trans
                )
                result = location.location_handler(all_locs_data)
                # Extract the result
                result = self.extract_response(result)
                # Create response message in case of fail
                msg = 'The output "{}" was not the fail response.'
                # Check whether the response is the same as the name
                self.assertTrue(
                    "unfortunately" in result.lower(),
                    msg.format(result))
            
        # Sanitize the data
        self.sanitize_input_data(all_locs_data)

    def test_direction_to(self):
        """
        This test check whether our _direction_to_ function works properly.
        It iterates through all possible combinations and checks if these give a proper
        response.
        """

        # Get the data from the test-JSON file
        dir_data = self.test_data.get('direction', {})

        # InputTranscripts for our test, we check both ways
        input_trans1 = 'how to get from {} to {}'
        input_trans2 = 'how to get to {} from {}'

        # To iterate through the list we convert it to a list
        set1 = list(self.locations.items())
        set_length = len(set1)

        for i in range(0, set_length):
            j = (i + 1) % set_length
            loc, loc2 = set1[i][0], set1[j][0]
            data, data2 = set1[i][1], set1[j][1]

            input1, input2 = input_trans1.format(loc, loc2), input_trans2.format(loc, loc2)

            event = self.input_values_to_location(dir_data, input1, loc, loc2)
            event1_response = location.location_handler(event)
            response1 = self.extract_response(event1_response)

            event2 = self.input_values_to_location(dir_data, input2, loc, loc2)
            event2_response = location.location_handler(event2)
            response2 = self.extract_response(event2_response)

            lat1, lon1 = data['lat'], data['lon']
            lat2, lon2 = data2['lat'], data2['lon']

            msg = "with locations {} and {}\n" \
                  "Response1 is equal to {}\n" \
                  "Response2 is equal to {}".format(
                        loc,
                        loc2,
                        response1,
                        response2)

            if not ((lat1 and lon1) and (lat2 and lon2)):
                self.assertTrue("Sorry" in response1, msg)
                self.assertTrue("Sorry" in response2, msg)
            else:
                self.assertTrue(response1.split(" ")[0] in loc2, msg)
                self.assertTrue(response2.split(" ")[0] in loc, msg)

    def test_direction_to_inputs(self):
        """
        This test checks whether _direction_to_ actually handles false input.
        """

        # Get the data from the test-JSON file
        dir_data = self.test_data.get('direction', {})

        # InputTranscript created
        input_trans = 'how to get from to {}'

        set0 = list(self.locations.items())
        set_len = len(set0)

        for i in range(0, set_len):
            loc = set0[i][0]
            data = set0[i][1]

            input0 = input_trans.format(loc)

            event = self.input_values_to_location(dir_data, input0, loc, None)
            event_response = location.location_handler(event)
            response = self.extract_response(event_response)

            msg = "With one location being 'None' (other being {}) we got an answer not containing 'Sorry'"

            self.assertTrue(
                "Sorry" in response,
                msg.format(loc)
            )
