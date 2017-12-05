import json
import urllib.request
from pprint import pprint

import xml.etree.ElementTree as ET

from datetime import datetime, timedelta

# More information from
# http://lassisavola.net/2016/02/04/fmi-avoin-data-python-ja-pylvasdiagrammit-osa-2/
# https://docs.python.org/2/library/xml.etree.elementtree.html

apikey = "eb3a4102-7afd-4740-8901-bf6417df01c3"

def format_time(time):
    temp = time[:time.find(':')+3] + 'Z'
    return temp


start_time = (datetime.now() - timedelta(hours=3)).isoformat()
end_time = (datetime.now() - timedelta(minutes=15)).isoformat()

time_str = '&starttime=' + format_time(start_time) + '&endtime=' + format_time(end_time)

place_str = 'otaniemi,espoo'
query_str = 'fmi::observations::weather::simple&place=' 
parameters_str = '&parameters=temperature'

url = "http://data.fmi.fi/fmi-apikey/"+apikey+"/wfs?request=getFeature&storedquery_id=" + query_str + place_str + time_str  + parameters_str
print(url)
datafile_url = '/tmp/' + "weather_data.xml"


def read_data():
    
    tree = ET.parse(datafile_url)
    root = tree.getroot()
    
    temperatures = {}
    temps = []
    
    for child in root:
        temp = child[0][3].text
        time = child[0][1].text
        print(time, temp)
        temperatures[time] = float(temp)
        temps.append(float(temp))

    return temps
    

def update_data(web_url, data_url):
    urllib.request.urlretrieve(web_url, data_url)

    
update_data(url, datafile_url)
