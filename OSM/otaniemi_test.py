from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import json
import requests

# These are some lats and longs of Otaniemi taken straight from the query URL in openstreetmat.org
# query?lat=60.1853&lon=24.8307#map=15/60.1842/24.8294

# And this query is taken straight from a help forum
#   https://help.openstreetmap.org/questions/19340/get-subregions-that-city-is-parent-of
# http://overpass-api.de/api/interpreter?data=rel[name=Helsinki];>;is_in;area._[admin_level];out;

xml = """
<query type="node">
  <has-kv k="name" v="Otaniemi"/>
</query>
<around radius="30"/>
<print/>
"""
#headers = {'Content-Type': 'application/xml'}
#print(requests.post('https://lz4.overpass-api.de/api/interpreter', data=xml, headers=headers).text)

nominatim = Nominatim()
# niemi = nominatim.query('Otaniemi')
niemi = nominatim.query('Helsinki')
# niemi = nominatim.query('NYC')

query = overpassQueryBuilder(area=niemi.areaId(), elementType='node', selector='"highway"="bus_stop"', out='body')

print(query)
print()

overpass = Overpass()
get = overpass.query(query)

elems = get.elements()
print(elems)
print(get.countElements())
print()
"""
nodes = get.nodes()
print(nodes)
print(len(nodes))
print()

ways = get.ways()
print(ways)
print(len(ways))
print()

ars = get.areas()
print(ars)
print(len(ars))
print()

with open('test.json', 'w+') as f:
    json.dump(get.toJSON(), f, indent=4)


result = overpass.query('way["name"="Dipoli"]; out body;')
print(result.elements())
"""
