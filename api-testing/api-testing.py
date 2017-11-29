
import requests, json

url = 'https://api.finna.fi/api/v1/'
headers = {'Accept': 'application/json'}
params = {'lookfor': 'softwareANDengineering', 'prettyPrint': '1'}#, 'limit': '1000'}

sess = requests.Session()
sess.headers.update(headers)
sess.params.update(params)

r = sess.request(url=url + 'search', method='POST')

js = r.json()

with open('data.json', 'w') as outfile:
    json.dump(js, outfile, indent=4)

sess.close()
