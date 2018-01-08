"""
This file attempts to introduce a user to the use of
the Finna API to search for needed results.

Documentation of the API can be found on the following link:
https://www.kiwi.fi/pages/viewpage.action?pageId=53839221

More technical documentation can be found on Swagger UI:
https://api.finna.fi/swagger-ui/?url=%2Fapi%2Fv1%3Fswagger#
"""

import requests
import json
import datetime
import os


""" This is the URL for the Finna API with a needed header for proper results """
url = 'https://api.finna.fi/api/v1/'
headers = {'Accept': 'application/json'}
json_dir = './api_testing/data_files/'


def do_request_json(term, method='GET', func='lookfor', pretty_print='0'):
    """
    Simple function for accessing the Finna API.
    :param term: what to look for, e.g. 'software'
    :param method: POST or GET, use of POST should be done if the reponse is long, defaults to GET
    :param func: the function the Finna API should use, defaults to 'lookfor'
    :param pretty_print: if the resulting JSON should be prettyprinted, '1' for yes and '0' for no, defaults to '0'
    :return: a dictionary with 'status_code' from the request and 'json'
    """
    params = {
        'id': 'fennica.123',  # TODO: this id might not be the right one (wait for AuthAPI)
        'prettyPrint': pretty_print,
        func: term
    }

    sess = requests.Session()
    sess.headers.update(headers)
    sess.params.update(params)

    r = sess.request(url=url + 'search', method=method)
    sess.close()

    return {'status_code': r.status_code, 'json': r.json()}


def do_request_file(term, method='GET', func='lookfor', pretty_print='0'):
    """
    Simple function for accessing the Finna API and creating a file for the response.
    :param term: what to look for, e.g. 'software'
    :param method: POST or GET, defaults to GET, use of POST should be done if the response is long
    :param func: the function the Finna API should use, defaults to 'lookfor'
    :param pretty_print: if the resulting JSON should be prettyprinted, '1' for yes and '0' for no, defaults to '0'
    :return: a dictionary with 'status_code' from the request and 'filename' of the file created
    """
    result = do_request_json(term, method, func, pretty_print)

    filename = 'data.json-' + str(datetime.datetime.now())
    filepath = json_dir + filename
    with open(filepath, 'w+') as output:
        if pretty_print == '1':
            json.dump(result['json'], output, indent=4)
        else:
            json.dump(result['json'], output)

    return {'status_code': result['status_code'], 'filename': filename}


def remove_json_files():
    """ Removes all JSON files in the `data_files` folder """
    for f in os.listdir(json_dir):
        if f.endswith('.json'):
            os.remove(os.path.join(json_dir, f))

