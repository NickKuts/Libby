import requests
import util
import re

"""This is the URL for the Finna API with a needed header for proper results"""
__url = 'https://api.finna.fi/api/v1/'
__headers = {'Accept': 'application/json'}
json_dir = './api_testing/data_files/'

translator = {
    'nonPresenterAuthors': 'authors',
    'publicationDates': 'published',

}


def parse(info):
    ret = []
    output = "Parse error"
    for elem in info:
        if 'name' in elem:
            ret.append(elem['name'])
            if len(ret) > 1:
                output = "Authors of this book is "
            else:
                output = "Author of this book is "
        elif re.compile('[0-9]{4}').match(elem):
            ret.append(elem)
            output = "This book was published in "
        else:
            if re.compile("1/AALTO/([a-z])*/"):
                ret.append(elem['translated'])
                output = "This book is located in "
    return output + util.make_string_list(ret)


def find_info(book_id, field='buildings'):
    request = record(book_id, {field, 'id'})['json']
    if request['status'] == 'OK':
        # print(request['json']['records'][0])
        field_info = request['records'][0][field]
        message = parse(field_info)
        return util.elicit_intent({'book_id': book_id}, message)
    else:
        return util.close({}, 'Fulfilled', "Something went wrong")


def subject_info(subject, extra_info=[]):
    request = lookfor(subject, filter=extra_info)['json']
    message = "Something went wrong"
    if request['status'] == 'OK':
        result_count = request['resultCount']
        if result_count == 0:
            message = "Sorry, no books was found with those search parameters "\
                      + subject
        elif result_count == 1:
            return find_info(request['records'][0]['id'])
        else:
            message = "With term " + subject + ", " + str(result_count) \
                      + " books was found. Could you give some more " \
                        "information about the book you are looking for? For " \
                        "example when the book is published or who is the " \
                        "author."
    return util.elicit_intent({'subject': subject}, message)


def extra_info(intent, extra_info=[]):
    subject = intent['sessionAttributes']['subject']
    input = intent['inputTranscript']
    lower = 0
    upper = 9999
    if re.search(r"between (\d{4}) and (\d{4})", input) is not None:
        lower = re.search(r"(\d{4}) and (\d{4})", input).group(1)
        upper = re.search(r"(\d{4}) and (\d{4})", input).group(2)
    elif re.search(r"before (\d{4})", input) is not None:
        upper = re.search(r"before (\d{4})", input).group(1)
        # print("<-" + str(re.search(r" before (\d{4})", input).group(1)))
    elif re.search(r"after (\d{4})", input) is not None:
        lower = re.search(r"after (\d{4})", input).group(1)
        # print(str(re.search(r" after (\d{4})", input).group(1)) + "->")
    elif re.search(r"(\d{4})", input) is not None:
        lower = re.search(r"(\d{4})", input).group(1)
        upper = re.search(r"(\d{4})", input).group(2)
    else:
        print("No year was given")
    date = "search_daterange_mv:\"[" + str(lower) + "TO" + str(upper) + "]\""
    return subject_info(subject, extra_info=[date])


def record(id, field={}, method='GET', pretty_print='0'):
    """
        Simple function for accessing the Finna API.
        :param id: id of the book looked for
        :param field: what fields we want to include in the json search
        :param method: POST or GET, use of POST should be done if the
        response is long, defaults to GET
        :param pretty_print: if the resulting JSON should be prettyprinted, '1'
        for yes and '0' for no, defaults to '0'
        :return: a dictionary with 'status_code' from the request and 'json'
        """
    params = {
        'field[]': field,
        'id': id,
        'prettyPrint': pretty_print,
    }

    sess = requests.Session()
    sess.headers.update(__headers)
    sess.params.update(params)

    r = sess.request(url=__url + 'record', method=method)
    sess.close()

    # print(r.url)
    # print(r.json())

    return {'status_code': r.status_code, 'json': r.json()}


def lookfor(term="", field=[], filter=[], method='GET', pretty_print='0'):
    """
    Simple function for accessing the Finna API.
    :param term: what to look for, e.g. 'software'
    :param field: what fields we want to include in the json search
    :param filter: filters the json search
    :param method: POST or GET, use of POST should be done if the reponse is
    long, defaults to GET
    :param pretty_print: if the resulting JSON should be prettyprinted, '1' for
    yes and '0' for no, defaults to '0'
    :return: a dictionary with 'status_code' from the request and 'json'
    """
    params = {
        'filter[]': [
            'building:"0/AALTO/"',
            'lng:en-gb'
        ] + filter,
        'field[]': field,
        'prettyPrint': pretty_print,
        'lookfor': term,
    }

    sess = requests.Session()
    sess.headers.update(__headers)
    sess.params.update(params)

    r = sess.request(url=__url + 'search', method=method)
    sess.close()

    print(r.url)
    # print(r.json())
    print("result count: " + str(r.json()['resultCount']))

    return {'status_code': r.status_code, 'json': r.json()}


def prettyprint(input):
    return input['dialogAction']['message']['content']


print(prettyprint(find_info('publicationDates', lookfor('computer', [
    'publicationDates', 'id'])['json']['records'][0]['id'])))
print(prettyprint(find_info('nonPresenterAuthors', lookfor('computer')['json'][
    'records'][10]['id'])))
print(prettyprint(subject_info('corporate communication',)))
