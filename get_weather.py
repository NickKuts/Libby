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

time_str = '&starttime=2017-12-04T14:30Z&endtime=2017-12-04T15:50Z'
query_str = 'fmi::observations::weather::simple&place=otaniemi,espoo'
parameters_str = '&parameters=temperature'

url = "http://data.fmi.fi/fmi-apikey/eb3a4102-7afd-4740-8901-bf6417df01c3/wfs?request=getFeature&storedquery_id=" + query_str + time_str + parameters_str




datafile_url = "weather_data.xml"



def read_data():
    tree = ET.parse(datafile_url)
    root = tree.getroot()

    results = tree.findall('{http://www.opengis.net/wfs/2.0}ParameterValue')
    print(results)
    print("itse juttu")
    
    for child in root.findall('{http://www.opengis.net/wfs/2.0}member'):
        #print(child.tag, child.attrib)
        for c in child:
            #print(c.tag, c.attrib)
            #print(c)
            for cc in c:
                testi = "{http://xml.fmi.fi/schema/wfs/2.0}"
                print(cc.tag)
                print(cc.get(testi + 'ParameterValue'))
                print(cc.find('{http://www.opengis.net/wfs/2.0}ParameterValue'))
                #print(cc.get('temperature'))

def update_data(web_url, data_url):
    urllib.request.urlretrieve(web_url, data_url)

#update_data(url, datafile_url)
read_data()
