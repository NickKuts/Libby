from difflib import SequenceMatcher
from math import cos, sin, pi, atan2, sqrt


directions = {
    (337.5, 360)   : "North", 
    (0, 22.5)      : "North", 
    (22.5, 67.5)   : "North-East", 
    (67.5, 112.5)  : "East", 
    (112.5, 157.5) : "South-East", 
    (157.5, 202.5) : "South", 
    (202.5, 247.5) : "South-West", 
    (247.5, 292.5) : "West", 
    (292.5, 337.5) : "North-West"
}


def direction(angle):
    print(angle)
    for key in directions:
        if in_range(angle, key[0], key[1]):
            return directions[key]


def distance(lat1, lon1, lat2, lon2):
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

    lat1, lon1, lat2, lon2 = map(to_radians, (lat1, lon1, lat2, lon2))

    delta_lon = lon2 - lon1

    y = sin(delta_lon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon)

    brng = atan2(y, x)
    brng = brng * 180 / pi
    brng = (brng + 360) % 360
    return brng


def to_radians(degs):
    return degs * pi / 180


def in_range(angle, mini, maxi):
    return (mini <= angle) and (angle <= maxi)


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

    param: s1 the first string for the comparison
    param: s2 the second string for the comparison
    return: returns an `int` representing the "closeness" of the strings
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

