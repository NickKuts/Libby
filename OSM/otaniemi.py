from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import json

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
