"""
This file attempts to introduce a user to the use of
the Finna API to search for needed results.
"""

import requests
import json
import datetime


url = 'https://api.finna.fi/api/v1/'
headers = {'Accept': 'application/json'}


def do_request(term, method='GET', func='lookfor', pretty_print='0'):
    """
    Simple function for accessing the Finna API.
    :param term: what to look for, e.g. 'software'
    :param method: POST or GET, defaults to GET, use of POST should be done if the response is long
    :param func: the function the Finna API should use, defaults to 'lookfor'
    :param pretty_print: if the resulting JSON should be prettyprinted, '1' for yes and '0' for no, defaults to '0'
    """
    params = {
        'id': 'fennica.123',
        func: term,
        'prettyPrint': pretty_print
    }

    sess = requests.Session()
    sess.headers.update(headers)
    sess.params.update(params)

    r = sess.request(url=url + 'search', method=method)

    _json = r.json()
    with open('data.json' + str(datetime.datetime.now()), 'w') as output:
        if pretty_print == '1':
            json.dump(_json, output, indent=4)
        else:
            json.dump(_json, output)
    sess.close()


do_request('software', pretty_print='1')
