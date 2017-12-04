import json
import urllib.request
from pprint import pprint
import xml.etree.ElementTree as ET

import datetime

# More information from
# http://lassisavola.net/2016/02/04/fmi-avoin-data-python-ja-pylvasdiagrammit-osa-2/

apikey = "eb3a4102-7afd-4740-8901-bf6417df01c3"
place = "otaniemi,Espoo"
url = "http://data.fmi.fi/fmi-apikey/" + apikey + "/wfs?request=getFeature&storedquery_id=fmi::forecast::hirlam::ground::point::timevaluepair&place=" + place + "/"
url2 = "http://data.fmi.fi/fmi-apikey/eb3a4102-7afd-4740-8901-bf6417df01c3/wfs?request=getFeature&storedquery_id=fmi::forecast::hirlam::ground::point::timevaluepair&place=jaala/"

date = '2017-12-03'
time = datetime.datetime.now().isoformat()
url = "http://data.fmi.fi/fmi-apikey/eb3a4102-7afd-4740-8901-bf6417df01c3/wfs?request=getFeature&storedquery_id=fmi::observations::weather::simple&place=otaniemi,espoo"

datafile_url = "weather_data.xml"



def read_data():
    tree = ET.parse(datafile_url)
    root = tree.getroot()

    for child in root.findall('{http://www.opengis.net/wfs/2.0}member'):
        #print(child.tag, child.attrib)
        for c in child:
            print(c.tag, c.attrib)

def update_data(web_url, data_url):
    urllib.request.urlretrieve(web_url, data_url)

update_data(url, datafile_url)
read_data()
