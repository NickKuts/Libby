import json
import difflib


# Open the JSON file containing all restaurant information
locations_json = 'locations.json'
with open(locations_json, 'r') as fp:
    locations = json.load(fp)
    
    
def _existence(name):
    """
    This function checks if the location can be found on disk, if not return None.
    """
    for loc in locations:
        location = locations[loc]
        aliases = location['aliases']
        for al in aliases:
            if name in al:
                return location
    return None


def address(event):
    """
    This function returns the address of the location the user asks for.
    """
    addr = "Sorry, I could not find address for that location"
    name = return_name(event)
    
    if not name:
        return addr
        
    info = _existence(name)
    if name:
        return 'The address of {} is {}'.format(name, info['address'].capitalize())
    
    return addr
    
    
def return_name(event):
    """
    This function simply returns the name of the location found in the query, if it exists.
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
    E.g. if the query of the user contains address the query is routed to the 'address' 
    function that finds the address.
    """
    if 'address' in trans:
        return address
    return return_name
    

def location_handler(event):
    """
    This is the handler function for the Location intent.
    """
    trans = event['inputTranscript']
    func  = checker(trans)
    ans   = func(event)
    
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

