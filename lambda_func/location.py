import json
import difflib
import re


# Open the JSON file containing all restaurant information
locations_json = 'locations.json'
with open(locations_json, 'r') as fp:
    locations = json.load(fp)
    
    
def _existence(name):
    """
    This function checks if the location can be found on disk, 
    if not return None.
    """
    for loc in locations:
        location = locations[loc]
        aliases = location['aliases']
        for al in aliases:
            if name in al: return location
    return None


def address(name, data):
    """
    This function returns the address of the location the user asks for.
    """
    addr = "Sorry, I could not find an address for that location"
    
    if not data:
        return addr

    find_addr = data.get('address', None)
    if find_addr:
        return 'The address of {} is {}'.format(
                        name, find_addr.capitalize())


def open_hours(name, data):
    """ 
    Simple function for returning opening hours of buildings, 
    if they have them.
    """
    hours = 'Sorry, I could not find any opening hours for this location'

    if not data:
        return hours

    find_hours = data.get('opening_hours', None)
    if find_hours:
        return 'The opening hours for {} are the following: {}'.format(
                        name, find_hours)
    
    
def return_name(event):
    """
    This function simply returns the name of the location found in the query, 
    if it exists.
    If the slot does not exist the function simply returns '(unknown)'.
    """
    slots = event['currentIntent']['slots']
    val   = None
    
    for slot in slots:
        temp = slots[slot]
        if temp:
            val = temp
            
    return val
    

def checker(trans):
    """
    This function finds the correct function for the answer.
    E.g. if the query of the user contains address the query is routed to the   
    'address' function that finds the address.
    """
    if 'address' in trans:
        return address
    elif 'where is' in trans:
        return address
    elif 'open' in trans:
        return open_hours
    return return_name


def parse_trans(trans):
    """ Parse inputTranscript """
    return ''
    

def location_handler(event):
    """
    This is the handler function for the Location intent.
    """
    trans = event['inputTranscript']
    func  = checker(trans)
    
    name = return_name(event)
    name = name if name else parse_trans(trans)

    data = _existence(name)
    ans  = func(name, data) if data else None

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


