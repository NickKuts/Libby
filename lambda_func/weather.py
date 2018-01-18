from . import util
import urllib3
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os


# More information from
# http://lassisavola.net/2016/02/04/fmi-avoin-data-python-ja-pylvasdiagrammit-osa-2/
# https://docs.python.org/2/library/xml.etree.elementtree.html
'''
This class can be used to get weather data (currently only temperature) from ilmatieteenlaitos
'''
class Weather:

    def format_time(self, time):
        temp = time[:time.find(':')+3] + 'Z'
        return temp

    def __init__(self):
        self.api_key = ""

        self.api_key = os.getenv('fmi_api')

        self.start_time = (datetime.now() - timedelta(hours=3)).isoformat()
        self.end_time = (datetime.now() - timedelta(minutes=15)).isoformat()
        
        self.time_str = '&starttime=' + self.format_time(self.start_time) + '&endtime=' + self.format_time(self.end_time)
        self.place_str = 'otaniemi,espoo'
        self.query_str = 'fmi::observations::weather::simple&place='
        self.parameters_str = '&parameters=temperature'
        
        self.url = "http://data.fmi.fi/fmi-apikey/" + self.api_key + "/wfs?request=getFeature&storedquery_id=" + self.query_str + self.place_str + self.time_str + self.parameters_str
        self.fname = '/tmp/' + "weather_data.xml"

    '''
    Read data from weather_data.xml
    '''
    def read_data(self):
        self.update_data(self.url, self.fname)
        tree = ET.parse(self.fname)
        root = tree.getroot()

        temperatures = {}
        temps = []

        for child in root:
            temp = child[0][3].text
            time = child[0][1].text
            # print(time, temp)
            temperatures[time] = float(temp)
            temps.append(float(temp))

        return temps

    '''
    Update the weather data
    '''
    def update_data(self, web_url, data_url):
        # print(web_url)
        # print(data_url)
        urllib3.urlretrieve(web_url, data_url)


def weather_handler():
    weather = Weather
    data = weather.read_data()

    # card_title = "Weather in otaniemi"
    message = {
        'contentType': 'PlaintText',
        'content': "The temperature is around " + str(data[0])
    }
    return util.close({}, 'Fulfilled', message)


