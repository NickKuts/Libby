#!/usr/bin/env python3.6

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.api import Api
import json
import requests


_osm_api = Api()
_nominatim = Nominatim()
_otaniemi_query = _nominatim.query('Otaniemi')
_otaniemi = _otaniemi_query.toJSON()
print(_otaniemi)


def get_restaurants(f_p):
    """ 
    Function for getting all restaurants from the Useful Aaltomap JSON file. 
    The function saves both the name of the restaurant, as well as the equivalent OSM node id
    """
    restaurants = {}
    aalto = json.load(f_p)

    def add_child(ch):
        """ Helper function for including child nodes to `restaurants` """
        if 'type' in ch and ch['type'] == 'restaurant':
            if 'name' in ch:
                restaurants[ch['name']] = c['osm'].replace('=', '/')
            else:
                restaurants[ch['id'].title()] = c['osm'].replace('=', '/')

    # The JSON file has (for some reason) separated restaurants into two JSON variables,
    # thus we have to got through both
    for v in aalto['buildings']:
        if 'children' in v:
            child = v['children']
            for c in child:
                add_child(c)
    for v in aalto['other']:
        add_child(v)
    return restaurants


def save_restaurants(rests, filename='restaurants.json'):
    """ Quick function for saving all restaurants found in UsefulAaltoMap """
    if not filename.endswith('.json'):
        filename = filename + '.json'
    with open(filename, 'w+') as f_p:
        json.dump(rests, f_p, indent=4)


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


def otaniemi():
    xml = """
    <query type="node">
        <has-kv k="name" v="Otaniemi"/>
    </query>
    <around radius="3"/>
    <print/>
    """
    headers = {'Content-Type': 'application/xml'}
    query = requests.post(
        'https://lz4.overpass-api.de/api/interpreter',
        data=xml,
        headers=headers
    )
    print(query.text)


def reformat(data):
    pass


def aaltomap_handler(event, context):
    """ Handler function for the AWS Lambda function """
    filename = event['filename']

    with open(filename, 'r') as f:
        restaurants = get_restaurants(f)

    #print(get_rest_location(list(restaurants.values())[0]))
    #save_restaurants(restaurants)
    #import util.py
    #return util.close({}, 'Fulilled', restaurants)
    return {
        'sessionAttributes': {},
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'content': restaurants,
            }
        }
    }

