from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass


def testuing():
    nominatim = Nominatim()
    hels = nominatim.query('Helsinki')
    
    query = overpassQueryBuilder(
        area=hels.areaId(),
        elementType='node',
        selector='"highway"="bus_stop"',
        out='body'
    )
    
    overpass = Overpass()
    get = overpass.query(query)

    return get.countElements()


def handler(event, context):
    elems = testuing()

    return {
        'sessionAttributes': {},
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': str(elems),
            }
        }
    }

