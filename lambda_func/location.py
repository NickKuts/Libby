from OSMPythonTools.api import Api
import json

_osm_api = Api()
with open("restaurants.json", "r") as fp:
    restaurants = json.load(fp)


def get_tags(node):
    """
    Function for getting tags related to a certain restaurant
    :param node: the restaurant node
    :return: associated tags
    """
    if 'node=' in node:
        node.replace("=", "/")  # The string format has to be 'node/<id>'
    elif 'node' not in node:
        node = 'node/' + node
    return _osm_api.query(node).tags()


def location_handler(intent):
    slots = intent['currentIntent']['slots']
    val = '(unknown)'

    for slot in slots:
        temp = slots[slot]
        if temp:
            val = get_tags(restaurants[temp.lower()])
#            val = '{} {}'.format(val['addr:street'], val['addr:housenumber'])

    return {
        'sessionAttributes': {},
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': {
                'contentType': 'PlainText',
                'content': val
            }
        }
    }
