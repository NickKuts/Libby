from urllib.request import Request, urlopen
import json
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


def parse_record(info):
    ret = []
    output = "Parse error"
    for elem in info:
        print("elem: " + str(elem))
        if 'name' in elem:
            ret.append(elem['name'])
            if len(ret) > 1:
                output = "Authors of this book is "
            else:
                output = "Author of this book is "
        elif re.compile('[0-9]{4}').match(str(elem)):
            ret.append(elem)
            output = "This book was published in "
        else:
            print("elem: " + elem['value'])
            if re.compile("1/AALTO/([a-z])*/").match(elem['value']):
                ret.append(elem['translated'])
                output = "This book is located in "
    return output + util.make_string_list(ret)


def find_info(book_id, field='buildings'):
    request = record(book_id, {field: 'id'})['json']
    if request['status'] == 'OK':
        # print(request['json']['records'][0])
        field_info = request['records'][0][field]
        message = parse_record(field_info)
        return util.elicit_intent({'book_id': book_id}, message)
    else:
        return util.close({}, 'Fulfilled', "Something went wrong1")


def parse_subject(request, subject):
    message = "Something went wrong2"
    if request['status'] == 'OK':
        result_count = request['resultCount']
        if result_count == 0:
            message = "Sorry, no books was found with those search terms"\
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


def subject_info(subject, extra_info=[]):
    if subject.startswith("find"):
        subject = subject[5:]
    if subject.endswith("book") or subject.endswith("books"):
        subject = subject[:-5]

    request = lookfor(term=subject, filter=extra_info)['json']
    #print("subject: " + subject)
    # print("extra_info: " + extra_info())
    #print("request: " + json.dumps(request))
    return parse_subject(request, subject)


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


def record(id, field=[], method='GET', pretty_print='0'):
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
        'id': [id],
        'prettyPrint': [pretty_print],
        'lng': ['en-gb']
    }

    params_str = []
    for key, value in params.items():
        for term in value:
            add_str = key + "=" + term
            params_str.append(add_str)
    # print(str(params_str))

    url_data = __url + 'record?' + "&".join(params_str)
    webURL = Request(url_data)
    webURL.add_header('User-Agent', 'Mozilla/5.0')
    data = urlopen(webURL).read()
    # print(data)
    encoding = webURL.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))

    print(url_data)
    # print(JSON_object)
    # print("result count: " + str(JSON_object['resultCount']))

    return {'status_code': JSON_object['status'], 'json': JSON_object}


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
        'lookfor': [term],
        'filter[]': [
            'building:"0/AALTO/"',
        ] + filter,
        'field[]': field,
        'prettyPrint': [pretty_print],
        'lng': ['en-gb']
    }

    params_str = []
    for key, value in params.items():
        for term in value:
            add_str = key + "=" + term
            params_str.append(add_str)
    # print(str(params_str))
    url_data = __url + 'search?' + "&".join(params_str)
    webURL = urlopen(url_data)
    data = webURL.read()
    # print(data)
    encoding = webURL.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))

    print(url_data)
    # print(JSON_object)
    # print("result count: " + str(JSON_object['resultCount']))

    return {'status_code': JSON_object['status'], 'json': JSON_object}


def prettyprint(input):
    return input['dialogAction']['message']['content']
