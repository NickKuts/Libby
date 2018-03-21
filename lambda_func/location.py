import json
import re
from location_utils import ratio


# Open the JSON file containing all restaurant information
_locations_json = 'locations.json'
with open(_locations_json, 'r') as fp:
    _locations = json.load(fp)


# Regex pattern for use in parser
_re_patt = r'(?P<location>.+)'

# Open the JSON file containing all sample utterances
_sample_utts = 'sample_utterances.json'
with open(_sample_utts, 'r') as fp:
    _samples = json.load(fp)

# Set all utterances to be regex patterns
for i in range(0, len(_samples)):
    reg_str = _samples[i].replace('{place}', _re_patt)
    _samples[i] = re.compile(reg_str)
    
    
def _existence(name):
    """
    This function checks if the location can be found on disk, 
    if not return None.
    """
    curr = None
    score = 0
    name = name.lower()
    for loc in _locations:
        location = _locations[loc]
        aliases = location['aliases']
        for al in aliases:
            temp = ratio(al, name)
            if temp > score:
                curr = location
                score = temp

    return curr


def address(event):
    """
    This function returns the address of the location the user asks for.
    """
    addr = "Sorry, I could not find an address for that location"

    name, data = _process_name(event)
    
    if not data:
        return None

    find_addr = data.get('address', None)
    if find_addr:
        return 'The address of {} is {}'.format(
                        name, find_addr.capitalize())

    return addr


def open_hours(event):
    """ 
    Simple function for returning opening hours of buildings, 
    if they have them.
    """
    hours = 'Sorry, I could not find any opening hours for this location'

    name, data = _process_name(event)

    if not data:
        return None

    find_hours = data.get('opening_hours', None)
    if find_hours:
        return 'The opening hours for {} are the following: {}'.format(
                        name, find_hours)

    return hours
    
    
def _return_name(event):
    """
    This function simply returns the name of the location found in the query, 
    if it exists.
    If the slot does not exist the function simply returns None.
    """
    slots = event['currentIntent']['slots']
    val = None
    
    for slot in slots:
        temp = slots[slot]
        if temp:
            val = temp
            
    return val
    

def _checker(trans):
    """
    This function finds the correct function for the answer.
    E.g. if the query of the user contains address the query is routed to the   
    'address' function that finds the address.
    """
    def helper(strings):
        """ 
        Helper function for checking if a any from list of strings are
        contained in the inputTranscript
        """
        for st in strings:
            if st in trans:
                return True
        return False

    # Create a list with strings that should lead to the address function 
    # being used
    address_str = ['address', 'where is', 'location']

    if helper(address_str):
        return address
    """
    if 'address' in trans:
        return address
    elif 'where is' in trans:
        return address
    elif 'location' in trans:
        return address
    """
    if 'open' in trans:
        return open_hours
    return lambda event: _process_name(event)[0]


def _parse_trans(trans):
    """ 
    Parse inputTranscript.
    This function is used when Amazon Lex is not capable of finding the 
    correct slot value for an input. The function utilizes all sample
    utterances (that it assumes have been processed already, i.e. put
    as regex patterns) and checks through the inputTranscript with
    regex patterns consisting of these utterances. However, some 
    utterances may be very similar, so the function saves all matches
    and the corresponding regex pattern to then run the longest found
    string through all regex patterns. This shaves of "unnecessary" parts
    of each string.
    param: trans the inputTranscript to be parsed
    """
    
    # Save all matches here, they should be saved as tuples where the first
    # element is the regex pattern and the second the string found
    matches = []

    # Go through each regex pattern
    for sample in _samples:
        m = sample.fullmatch(trans)
        # The regex pattern is built such that the "found" building is saved
        # under the parameter name '_locations'
        if m:
            try:
                # We need to use a try-catch as some regex patterns from the 
                # sample utterances do not have the "string-finding" part, so
                # no 'location' is found.
                matches.append((sample, m.group('location')))
            except IndexError: 
                pass

    # Sort the array in-place, we need the longest string first so that the 
    # "shaving" works properly
    matches.sort(key=lambda t: len(t[1]), reverse=True)
    # Use an empty string placeholder in case no matches were found
    longest = ''

    # There should never be a case where no regex pattern matches, however, 
    # better safe than sorry
    if len(matches) > 0:
        longest = matches[0][1]
        for reg in matches:
            # Here is where the shaving happens, the longest string gets put
            # through "stricter" regex patterns to that all unnecessities
            # diminish
            m = reg[0].fullmatch(longest)
            if m:
                try:
                    # Same as above
                    longest = m.group('location')
                except IndexError:
                    pass
    
    # And finally return the shaved longest string (if such was found)
    return longest


def _process_name(event):
    """ Helper function for some of the functions above """
    name = _return_name(event)
    name = name if name else _parse_trans(event['inputTranscript'].lower())
    data = _existence(name)

    return name, data
    

def location_handler(event):
    """
    This is the handler function for the Location intent.
    """
    trans = event['inputTranscript']
    func = _checker(trans)
    
    ans = func(event)

    # Default answer if all failed
    if not ans:
        ans = "Unfortunately I can't seem to find the location"
    
    return {
        'sessionAttributes': {},
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': {
                'contentType': 'PlainText',
                'content': ans
            }
        }
    }
