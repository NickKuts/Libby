#!/usr/bin/env python3

import json


file_name = 'locations.json'
with open(file_name, 'r') as fp:
    locations = json.load(fp)

for loc, data in locations.items():
    building = data['building']
    if building:
        building = locations[building]

        addr = data['address']
        if not addr:
            locations[loc]['address'] = building['address']

        lon = data['lon']
        lat = data['lat']
        if not (lon and lat):
            locations[loc]['lon'] = building['lon']
            locations[loc]['lat'] = building['lat']

    pars = data['parents']
    if len(pars) > 0 and not locations[loc]['address']:
        for par in pars:
            curr = locations.get(par, None)
            if curr and not locations[loc]['address']:
                locations[loc]['address'] = curr['address']

with open(file_name, 'w') as fp:
    json.dump(locations, fp, indent=4)

