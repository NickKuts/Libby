import util
import re
import json
from botocore.vendored import requests
import author_search as AS
from itertools import takewhile


"""This is the URL for the Finna API with a needed header for proper results"""
__url = 'https://api.finna.fi/api/v1/'
__headers = {'Accept': 'application/json'}
json_dir = './api_testing/data_files/'


"""
   AWS INPUT(SEARCH TERM)                     ->parse_subject()-->OUTPUT TO AWS
                         \                   /           |        A        
                          \                 /            |       /
                           \               /             V      /
                            ->subject_info()          find_info()<==>record()
                                  A                     |  A
                                  |                     |  |
                                  |                     V  |
    AWS INPUT(EXTRA INFO)--->extra_info()              parse_book()
"""


def parse_book(info):
    """
    Parses the record's data and constructs a message from the data. Wanted
    info is given as a parameter in JSON format. Default info is data
    about the location(library) of the book.
    :param info: Data of wanted info in JSON format
    :return: Message constructed from the data
    """
    ret = []
    output = "Parse error"
    print("info", info)
    for elem in info:
        # print("elem: " + str(elem))
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
        # print("elem: " + elem['value'])
        if re.compile("1/AALTO/([a-z])*/").match(elem['value']):
            ret.append(elem['translated'])
            output = "This book is located in "
        if re.compile("0/AALTO/([a-z])*").match(elem['value']):
            ret.append(elem['translated'])
            output = "This book is located in "
    return output + util.make_string_list(ret)


def find_info(book_id, field='buildings'):
    """
    :param book_id: Id of the book
    :param field: Field which teh user is looking for
    :return: Response to AWS server in JSON format
    """
    print("id", book_id)
    request = record(book_id, field=['id', field])['json']
    print("count", request['resultCount'])
    if request['status'] == 'OK':
        # print(request['json']['records'][0])
        field_info = request['records'][0][field]
        message = parse_book(field_info)
        return util.elicit_intent({'book_id': book_id}, message)
    else:
        return util.close({}, 'Fulfilled', "Something went wrong")


def parse_subject(request, subject, author=None):
    """
    :param request: JSON data from the Finna API
    :param subject: Subject or search term of the current session
    :return: Response to AWS server in JSON format
    """
    message = "Something went wrong"
    if subject is "":
        return util.elicit_intent({}, "I'm sorry. I was not able to catch "
                                      "what book you wanted to find. Could "
                                      "you please repeat.")
    # if request['status'] == 'no info':
    # message = "No extra info was found222"
    if request['status'] == 'OK':
        result_count = request['resultCount']
        print("result parse subject ", result_count)
        print("subject ", subject)
        
        if result_count == 0: 
            message = "Oh I'm so sorry, no books was found with search term: " + subject
            if author:
                message += " written by " + str(author)

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

            if author:
                message = subject + " books by " + str(author) \
                      + " can be found in " + util.make_string_list(find)
            else:
                message = subject + " books can be found in " + \
                      util.make_string_list(find)
 
        else:
            if not author:
                message = "I found " + str(result_count) + " books with term " \
                          + subject + ". Please specify an author or a year, so" \
                          " I can narrow down the earch."
            else:
                message = "I found " + str(result_count) + " books with " \
                          + subject + " by author " + author + ". Can you give" \
                          " the publication date for example to narrow down" \
                          " the search."
 
    return util.elicit_intent({'subject': subject}, message)


def subject_info(intent, extra_info=[]):
    """
    :param intent: the input intent
    :param extra_info: Given parameters to filter the data
    :return: Response to AWS server in JSON format
    """
    print("=========subject info============")

    text = intent['inputTranscript'].lower()
    utterances = AS.load_file('sample_utterances.txt')

 
    for line in list(utterances):
        utterances += line + " book "
        utterances += line + " books "

    to_drop = 0

    for line in utterances:
        if text.startswith(line):
            to_drop = len(line)
            break
    text = text[to_drop:].strip()
    text_list = text.split(' ', len(text))

    print("text_list: ", str(text_list))

    subject_list = []
    keywords = ["books", "book", "by", "published", "written"]
    keyword = ""

    # Find when the book name ends

    for word in text_list:
        if word not in keywords:
            subject_list.append(word)
        else:
            keyword = word
            break

    subject = " ".join(subject_list)
    print("-------" + subject + "--------")

    print("subject: ", subject)
    author_text = text[len(subject) + 1 + len(keyword):].strip()

    # The idea of this part of the code is to drop 'by' out 
    # because if the user say 'written by', only written is 
    # dropped in the code above.
    author_text_list = author_text.split(' ', len(author_text))
    
    if author_text_list[0] == 'by':
        author_text = author_text[3:]
    
    author = find_author(author_text)
    
    print("Author:", author)
    print("extra info", extra_info)
   
    # There might be old info in the extra_info (author), so 
    # we need to clear it
    extra_info.clear()

    if author:
        extra_info += [
            "author:\"" + author + "\""
        ]

    request = lookfor(term=subject, filter=extra_info)['json']
    print("___result count___:", request['resultCount'], subject)
    
    return parse_subject(request, subject, author)


def extra_info(intent):
    """
    :param intent: Input from AWS servers
    :return: Response to AWS server in JSON format
    """
    subject = intent['sessionAttributes']['subject']
    slots = intent['currentIntent']['slots']
    input = intent['inputTranscript']
    lower = 0
    upper = 9999
    
    if 'lower' in slots or 'upper' in slots or 'year' in slots:
        if 'lower' in slots:
            if slots['lower']:
                lower = slots['lower']
        if 'upper' in slots:
            if slots['upper']:
                upper = slots['upper']
        if 'year' in slots:
            if slots['year']:
                lower = slots['year']
                upper = slots['year']
        date = "search_daterange_mv:\"[" + str(lower) + " TO " + str(
            upper) + "]\""
        extra_info = [date]
        request = lookfor(term=subject, filter=extra_info)['json']

        return parse_subject(request, subject) 
    else:
        return author_search(intent, subject)


def author_search(intent, subject):

    author = find_author(intent['inputTranscript'])

    if author:
        request = lookfor(subject, filter=["author:\"" + author + "\""])['json']
        return parse_subject(request, subject, author)

    return util.elicit_intent({'subject': subject},
                              "No extra information was given.")


def find_author(text):
    author = AS.search(text, False)
 
    return author


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
    # print(r.json())
    # print("result count: " + str(r.json()['resultCount']))
    return {'status_code': r.status_code, 'json': r.json()}
