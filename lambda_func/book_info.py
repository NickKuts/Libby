import util
import re
from botocore.vendored import requests

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
        """
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
        """
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
        return util.close({}, 'Fulfilled', "Something went wrong")


def parse_subject(request, subject):
    message = "Something went wrong"
    if request['status'] == 'OK':
        result_count = request['resultCount']
        if result_count == 0:
            message = "Sorry, no books was found with search term: "\
                    + subject
        elif result_count == 1:
            return find_info(request['records'][0]['id'])
        elif result_count < 5:
            real_count = 0
            find = []
            while real_count < result_count:
                buildings = request['records'][real_count]['buildings']
                for layer in buildings:
                    if re.compile("1/AALTO/([a-z])*/").match(layer['value']):
                        if layer['translated'] not in find:
                            find.append(layer['translated'])
                real_count += 1

            message = "With term " + subject + ", books can be found in " + util.make_string_list(find)
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
        subject = subject[:-5].strip()

    request = lookfor(term=subject, filter=extra_info)['json']
    # print("subject: " + subject)
    # print("extra_info: " + extra_info())
    # print("request: " + json.dumps(request))
    return parse_subject(request, subject)


def extra_info(intent):
    subject = intent['sessionAttributes']['subject']
    # input = intent['inputTranscript']
    slots = intent['currentIntent']['slots']
    lower = 0
    upper = 9999
    if slots['lower']:
        lower = slots['lower']
    if slots['upper']:
        upper = slots['upper']
    if slots['year']:
        lower = slots['year']
        upper = slots['year']
    """
    if re.search(r"between (\d{4}) and (\d{4})", input) is not None:
        # print("between")
        lower = re.search(r"(\d{4}) and (\d{4})", input).group(1)
        upper = re.search(r"(\d{4}) and (\d{4})", input).group(2)
    elif re.search(r"before (\d{4})", input) is not None:
        # print("before")
        upper = re.search(r"before (\d{4})", input).group(1)
    elif re.search(r"after (\d{4})", input) is not None:
        # print("after")
        lower = re.search(r"after (\d{4})", input).group(1)
    elif re.search(r"(\d{4})", input) is not None:
        # print("year")
        lower = re.search(r"(\d{4})", input).group(1)
        upper = re.search(r"(\d{4})", input).group(1)

    # if user's answer starts 'the book is written by'
    elif input.startswith('the book is written by'):
        written = input[22:]
        split_list = written.split()
        split_list = split_list[:2]
        with_com = ',+'.join(split_list)

       # count = lookfor(subject, filter=["author:\""+withCom+"\""])['json']['resultCount']
       # print("result count: " + str(count))
        if  lookfor(subject,filter=["author:\""+with_com+"\""])['json'][
                                                            'resultCount'] > 0:
            return subject_info(subject, extra_info=["author:\""+with_com+"\""])
        else:
            reversed_list = split_list[::-1]
            reversed_with_com = ', '.join(reversed_list)
            if lookfor(subject, filter=["author:\""+reversed_with_com+"\""])[
                                        'json']['resultCount'] > 0:
                return subject_info(subject, extra_info=[
                                            "author:\""+reversed_with_com+"\""])

    # if user's answer starts 'book is written by'
    elif input.startswith('book is written by'):
        written = input[18:]
        split_list = written.split()
        split_list = split_list[:2]
        with_com = ', '.join(split_list)

        if lookfor(subject, filter=["author:\""+with_com+"\""])['json'][
                                                            'resultCount'] > 0:
            return subject_info(subject, extra_info=["author:\""+with_com+"\""])
        else:
            reversed_list = split_list[::-1]
            reversed_with_com = ', '.join(reversed_list)
            if lookfor(subject, filter=["author:\""+reversed_with_com+"\""])[
                                        'json']['resultCount'] > 0:
                return subject_info(subject, extra_info=[
                                            "author:\""+reversed_with_com+"\""])

    else:
        print("No extra info was given")
    # print("lower: " + str(lower) + "      upper: " + str(upper))
    date = "search_daterange_mv:\"[" + str(lower) + " TO " + str(upper) + "]\""
    # print(date)
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

    sess = requests.Session()
    sess.headers.update(__headers)
    sess.params.update(params)

    r = sess.request(url=__url + 'record', method=method)
    sess.close()

    # print(r.url)
    # print(r.json())

    """
    params_str = []
    for key, value in params.items():
        for term in value:
            add_str = key + "=" + term
            params_str.append(add_str)
    # print(str(params_str))

    url_data = __url + 'record?' + "&".join(params_str)
    webURL = Request(url_data, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(webURL).read()
    # print(data)
    # encoding = webURL.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding='utf-8'))

    print(url_data)
    # print(JSON_object)
    # print("result count: " + str(JSON_object['resultCount']))

    return {'status_code': JSON_object['status'], 'json': JSON_object}
    """
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
        'lookfor': [term],
        'filter[]': [
            'building:"0/AALTO/"',
        ] + filter,
        'field[]': field,
        'prettyPrint': [pretty_print],
        'lng': ['en-gb']
    }

    sess = requests.Session()
    sess.headers.update(__headers)
    sess.params.update(params)

    r = sess.request(url=__url + 'search', method=method)
    sess.close()


    print(r.url)
    #print(r.json())
    # print("result count: " + str(r.json()['resultCount']))


    """
    params_str = []
    for key, value in params.items():
        for term in value:
            add_str = key + "=" + term
            params_str.append(add_str)
    # print(str(params_str))
    url_data = __url + 'search?' + "&".join(params_str)
    webURL = Request(url_data, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(webURL).read()
    # print(data)
    # encoding = webURL.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding='utf-8'))

    print(url_data)
    # print(JSON_object)
    # print("result count: " + str(JSON_object['resultCount']))

    return {'status_code': JSON_object['status'], 'json': JSON_object}
    """
    return {'status_code': r.status_code, 'json': r.json()}


