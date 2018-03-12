#!/usr/bin/env python3.6

import json
from OSMPythonTools.api import Api

api = Api()

with open('useful-aaltomap.json', 'r') as fp:
    aalto = json.load(fp)

def get_tags(osm, osm_meta):
    if not osm_meta and not osm:
        return None
    def do_query(st):
        return api.query(st).tags()
    query = None
    if osm_meta:
        if 'way' in osm_meta:
            query = osm_meta.replace('=', '/')
        if 'node' in osm_meta:
            query = osm_meta.replace('=', '/')
        if 'rel' in osm_meta:
            query = osm_meta.replace('rel=', 'relation/')
    if query:
        res = do_query(query)
        if len(res) > 0:
            return res
    if not osm:
        return None
    osm = str(osm)
    res = do_query('node/' + osm)
    if len(res) > 0:
        return res
    res = do_query('way/' + osm)
    if len(res) > 0:
        return res
    res = do_query('relation/' + osm)
    if len(res) > 0:
        return res
    return None

def process_data(data):
    if not data:
        return {}
    addr = None
    if 'addr:street' in data:
        addr = data['addr:street'] + ' ' + data.get('addr:housenumber', '')
    aliases = []
    if 'loc_name' in data:
        aliases.append(data['loc_name'])
    if 'name:en' in data:
        aliases.append(data['name:en'])
    opening_hours = data.get('opening_hours', None)
    return {
        'addr': addr,
        'aliases': aliases,
        'open_hours': opening_hours
    }

locations = {}
def add_child(ch, building=None, addr=None):
    name = ch.get('name', ch.get('id', None))
    if not name:
        print('No name or id: ' + ch)
        return

    tags = get_tags(ch.get('osm', None), ch.get('osm_meta', None))
    data = process_data(tags)
    locations[name] = {
        'aliases' : ch.get('aliases', []),
        'building': building,
        'address' : data.get('addr', addr),
        'osm'     : ch.get('osm', None),
        'osm_meta': ch.get('osm_meta', None),
        'opening_hours': data.get('open_hours', None),
        'type'    : ch.get('type', None)
    }

    row = locations[name]
    row['aliases'].append(name)
    if 'name_en' in ch:
        row['aliases'].append(ch['name_en'])
    row['aliases'] = row['aliases'] + data.get('aliases', [])
    row['aliases'] = list(map(lambda s: s.lower(), row['aliases']))


def go_through_doc(val):
    for l in aalto[val]:
        add_child(l)
    
        building = l.get('name', l['id'])
    
        if 'children' in l:
            child = l['children']
            for c in child:
                add_child(c, building, locations[building]['address'])

go_through_doc('buildings')
go_through_doc('other')

with open('test-loc.json', 'w+') as fp:
    json.dump(locations, fp, indent=4)

