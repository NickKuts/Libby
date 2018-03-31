from difflib import SequenceMatcher
from math import cos, sin, pi, atan2, sqrt
import re


directions = {
    (337.5, 360):   "North",
    (0, 22.5):      "North",
    (22.5, 67.5):   "North-East",
    (67.5, 112.5):  "East",
    (112.5, 157.5): "South-East",
    (157.5, 202.5): "South",
    (202.5, 247.5): "South-West",
    (247.5, 292.5): "West",
    (292.5, 337.5): "North-West"
}


def to_radians(degs):
    """
    A simple function for converting degrees to radians
    :param degs: degrees to be converted
    :return: the converted radians
    """
    return degs * pi / 180


def in_range(ang, mini, maxi):
    return (mini <= ang) and (ang <= maxi)


def direction(ang):
    """
    Checks the compass point of given angle. For if angle is equal to 0, the function returns north
    """
    for key in directions:
        if in_range(ang, key[0], key[1]):
            return directions[key]


def distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two locations that have longitude and latitude
    Returns value rounded to closest one meter
    """
    earth_radius = 6371000
    delta_lat = to_radians(lat2 - lat1)
    delta_lon = to_radians(lon2 - lon1)
    
    a = sin(delta_lat / 2) ** 2
    b = cos(to_radians(lat1)) * cos(to_radians(lat2))
    c = sin(delta_lon / 2) ** 2
    d = a + b * c

    e = 2 * atan2(sqrt(d), sqrt(1 - d))

    f = earth_radius * e
    return int(f)


def angle(lat1, lon1, lat2, lon2):
    """
    Calculates the angle between two points. Function treats lat1 and lon1 as a starting point
    and calculates the angle going clockwise (as a compass, i.e. from North).
    :param lat1: the latitude of the first location
    :param lon1: the longitude of the first location
    :param lat2: the latitude of the second location
    :param lon2: the longitude of the second location
    :return: the angle between the first and second location
    """
    lat1, lon1, lat2, lon2 = map(to_radians, (lat1, lon1, lat2, lon2))

    delta_lon = lon2 - lon1

    y = sin(delta_lon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon)

    brng = atan2(y, x)
    brng = brng * 180 / pi
    brng = (brng + 360) % 360
    return brng


def ratio(s1, s2):
    """
    This function is used to get a numerical value for how similar two strings
    are. It is inspired by the _fuzzywuzzy_ module, but as we are currently 
    only using the _ratio_ function from the module, we decided to recreate the
    function instead of including the whole module to the project. 

    If two strings are totally equal the answer will be `100`, and if they are
    totally unsimilar the answer will be `0`. However, as we created this 
    function "ourselves" for reason that we do not want to include external
    modules, the function is not commutative. This would require the module
    _python-Levensthein_ as explained in the _fuzzywuzzy_ GitHub pull request
    section: https://github.com/seatgeek/fuzzywuzzy/issues/173

    :param s1 the first string for the comparison
    :param s2 the second string for the comparison
    :return returns an `int` representing the "closeness" of the strings
    """

    # If any of the strings are `None` return `0`
    if s1 is None or s2 is None:
        return 0
    # If any of the strings have length `0`, return `0`
    if len(s1) == 0 or len(s2) == 0:
        return 0
    # If both of the strings are of type `str` they can be compared
    if isinstance(s1, str) and isinstance(s2, str):
        pass
    
    # Check if any of the parameters are of type `bytes`
    # if they are, decode them to strings (utf-8)
    if isinstance(s1, bytes):
        s1 = s1.decode('utf-8')
    if isinstance(s2, bytes):
        s2 = s2.decode('utf-8')

    # And finally we use `SequenceMatcher` to check for similarity 
    # in the strings
    m = SequenceMatcher(None, s1, s2)
    # Now, `m` above will be a `double`, so we convert it to `int`
    return int(round(100 * m.ratio()))


def parse_trans(trans, samples):
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
    :param trans: the inputTranscript to be parsed
    :param samples: the sample utterances that have been set to work with re
    :return: the extracted location name
    """
    
    # Save all matches here, they should be saved as tuples where the first
    # element is the regex pattern and the second the string found
    matches = []

    # Go through each regex pattern
    for sample in samples:
        m = re.search(sample, trans)
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
            m = re.search(reg[0], longest)
            if m:
                try:
                    # Same as above
                    longest = m.group('location')
                except IndexError:
                    pass
    
    # And finally return the shaved longest string (if such was found)
    return longest


def parse_trans_two(trans, n_samples):
    """
    This function is closely related to the _parse_trans_ function above.
    This function attempts to extract two locations from an input transcript.
    The reason for the separation are time constraints and that this function
    will only be used for one specific case in Location intent. For future
    ideas we might write them together, if time allows for it.
    Note: if anything in these comments (or below) is weirdly explained, please
          see the function _parse_trans_ above
    :param trans: the input transcript from Amazon Lex
    :param n_samples: sample utterances that have been regex compiled
    :return: the extraced location names
    """

    # We first extract those regex patterns that have two locations to find
    samples = filter(lambda reg: '<location2>' in reg, n_samples)

    # Save all matches here
    matches = []

    # Go through each regex pattern
    for sample in samples:
        m = re.search(sample, trans)
        # Extract each location
        if m:
            try:
                # For reasons of the 'try-catch', see the _parse_trans_ function
                matches.append((m.group('location'), m.group('location_two')))
            except IndexError:
                pass
    
    # Unfortunately we cannot do the same "shaving" as we did in _parse_trans
    # in this function, thus we only return the result that have the shortest
    # location names (as these are probably the closest to real answers)
    res = ('', '')
    for match in matches:
        if (len(match[0]) + len(match[1])) > (len(res[0]) + len(res[1])):
            res = match

    return res

