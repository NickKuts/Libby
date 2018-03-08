#!/usr/bin/env python3.6

import json
from .otaniemi import get_tags

with open('useful-aaltomap.json', 'r') as fp:
    aalto = json.load(fp)

locations = {}
def add_child(ch):
    if 'name' in ch:
        n = ch['name']
        locations[ch['name']] = (ch.get('type')

for l in aalto['buildings']:
    name = l['name'] if 'name' in l else l['id']

    locations[name] = {
        'aliases': l.get('aliases'),
        'building': None,




    if 'children' in l:
        child = l['location']
        for c in child:
            add_child(c)

