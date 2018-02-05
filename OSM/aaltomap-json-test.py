#!/usr/bin/env python3.6

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.api import Api
import json
import requests


_osm_api = Api()


def get_restaurants(f_p):
    """ 
    Function for getting all restaurants from the Useful Aaltomap JSON file. 
    The function saves both the name of the restaurant, as well as the equivalent OSM node id
    """
    restaurants = []
    aalto = json.load(f_p)
    # The JSON file has (for some reason) separated restaurants into two JSON variables,
    # thus we have to got through both
    for v in aalto['buildings']:
        if 'children' in v:
            child = v['children']
            for c in child:
                if 'type' in c and c['type'] == 'restaurant':
                    if 'name' in c:
                        restaurants.append((c['name'], c['osm'].replace("=", "/")))
                    else:
                        restaurants.append((c['id'].title(), c['osm'].replace("=", "/")))
    for v in aalto['other']:
        if 'type' in v and v['type'] == 'restaurant':
            restaurants.append((v['name'], v['osm'].replace("=", "/")))
    return restaurants


def get_rest_location(rest):
    """
    Function for getting tags related to a certain restaurant
    :param rest: the restaurant node
    :return: associated tags
    """
    if 'node=' in rest:
        rest.replace("=", "/")  # The string format has to be 'node/<id>'
    elif 'node' not in rest:
        rest = 'node/' + rest
    return _osm_api.query(rest).tags()


def otaniemi():
    xml = """
    <query type="node">
        <has-kv k="name" v="Otaniemi"/>
    </query>
    <around radius="300"/>
    <print/>
    """
    headers = {'Content-Type': 'application/xml'}
    query = requests.post(
        'https://lz4.overpass-api.de/api/interpreter',
        data=xml,
        headers=headers
    )
    print(query.text)


def aaltomap_handler(event, context):
    """ Handler function for the AWS Lambda function """
    filename = event['filename']

    with open(filename, 'r') as f:
        restaurants = get_restaurants(f)

    get_rest_location(restaurants[0][1])

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

