import util
import re
from botocore.vendored import requests
import author_search as AS
import signal


"""This is the URL for the Finna API with a needed header for proper results"""
__url = 'https://api.finna.fi/api/v1/'
__headers = {'Accept': 'application/json'}
json_dir = './api_testing/data_files/'


"""
   AWS INPUT(SEARCH TERM)---->subject_info()---->parse_subject()-->OUTPUT TO AWS
                                 A            A   |      |        A        
                                 |           /    |      |       /
                                 |          /     |      V      /
                                 | author_search()|   find_info()
                                 |    A           |     |  A
                                 |    |           |     |  |
                                 |    |           |     V  |
    AWS INPUT(EXTRA INFO)--->extra_info()         |  locate_book()
                                                  V
    AWS INPUT(AUTHOR INFO)--->find_info_author()---->parse_author()-->OUTPUT
"""


# Author intent use this.
def find_info_author(intent):
    text = intent['inputTranscript'].lower()
    utterances = AS.load_file('author_utterances.txt')
    to_drop = 0
    # this takes utterances off
    for line in utterances:
        if text.startswith(line):
            to_drop = len(line)
            break

    author_text = text[to_drop:].strip()

    # this checks that author exists
    author = AS.search(author_text, False)
    request = lookfor(term=author)['json']

    return parse_author(request, {'author': author})


def parse_author(request, session_attributes):
    """
    :param request: JSON data from the Finna API
    :param author: Author term of the current session
    :param session_attributes: session attributes for current session if user
    has given some
    :return: Response to AWS server in JSON format
    """

    # if author was not found
    author = session_attributes.get('author')
    if not author:
        message = "I'm sorry. I couldn't catch the author. Please try again."
        return util.elicit_intent({'author': author}, message)

    result_count = request['resultCount']

    # find all titles if title does not already exist in list. And sort them.
    real_count = 0
    find = []

    for record in request['records']:
        authors = record.get('nonPresenterAuthors')
        has_written = False
        for a in authors:
            # print(a.get('name').lower(), " == ", author)
            if a.get('name').lower() == author:
                # print("has written:", author)
                has_written = True
                break
        if has_written:
            title = record.get('title')
            if title:
                if title is not find:
                    find.append(title)
                    real_count += 1

    # at most three books
    find = sorted(find)
    print(str(find))
    if len(find) > 3:
        find = find[:3]
        find.append("others")

    # only one book was found
    if result_count == 1:
        message = author + " has written a book " + find[0]
    # many books was found
    else:
        message = author + " has written books " + util.make_string_list(find)
    return util.elicit_intent({'author': author}, message)


def locate_book(info):
    """
    Parses the record's data and constructs a message from the data. Wanted
    info is given as a parameter in JSON format. Default info is data
    about the location(library) of the book.
    :param info: Data of wanted info in JSON format
    :return: Message constructed from the data
    """
    ret = []
    output = "I'm sorry, there was an problem with this book in the " \
             "database"
    for elem in info:
        if re.compile("1/AALTO/([a-z])*/").match(elem['value']):
            ret.append(elem['translated'])
            output = " is located in "
        elif re.compile("0/AALTO/([a-z])*").match(elem['value']):
            ret.append(elem['translated'])
            output = " is located in "
        if len(ret) == 2:
            ret = ret[1:]
    return output + util.make_string_list(ret)


def find_info(book_id, field='buildings'):
    """
    Finds info from some book defined by book_id and constructs an output
    message. Default information searched is the building(and only
    information which can be searched atm).
    :param book_id: Id of the book
    :param field: Field which teh user is looking for
    :return: Response to AWS server in JSON format
    """
    request = record(book_id, field=['id', 'shortTitle', field])['json']
    if request['status'] == 'OK':
        message = locate_book(request['records'][0]['buildings'])
        title = request['records'][0]['shortTitle']
        message = "".join([title, message])
        return util.close({'book_id': book_id, 'author': None}, 'Fulfilled',
                                                                message)
    else:
        return util.close({'author': None}, 'Fulfilled', "Something went wrong")


def parse_subject(request, subject, session_attributes={}):
    """
    :param request: JSON data from the Finna API
    :param subject: Subject or search term of the current session
    :param session_attributes: session attributes for current session if user
    has given some
    :return: Response to AWS server in JSON format
    """
    author = session_attributes.get('author')
    if subject is "":
        if author:
            return parse_author(request, {'author': author})
        return util.elicit_intent(session_attributes, "I'm sorry. I was not "
                                                      "able to catch what book"
                                                      " you wanted to find. "
                                                      "Could you please repeat."
                                  )

    if request['status'] == 'OK':
        result_count = request['resultCount']

        if result_count == 0: 
            message = "Oh I'm so sorry, no books was found with search term: "\
                        + subject
            if author:
                message += " written by " + str(author)
            return util.close({'subject': subject, 'author': author},
                              'Fulfilled', message)

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
            return util.close({'subject': subject, 'author': author},
                              'Fulfilled', message)

        else:
            if not author:
                message = "I found " + str(result_count) + " books with term " \
                          + subject + ". Please specify an author or a year, " \
                                      "     so I can narrow down the search."
            else:
                message = "I found " + str(result_count) + " books with " \
                          + subject + " by author " + author + ". Can you " \
                          "give the publication date for example to narrow " \
                          "down the search."
            return util.elicit_intent({'subject': subject, 'author': author},
                                      message)
    else:
        return util.close({'author': None}, 'Fulfilled', "Something went wrong")


def subject_info(intent, extra_info=[]):
    """
    This function parses the input from AWS and finds the subject(search
    term) from the intent's inputTranscript.
    :param intent: the input intent
    :param extra_info: Given parameters to filter the data
    :return: Response to AWS server in JSON format
    """

    text = intent['inputTranscript'].lower()
    utterances = AS.load_file('sample_utterances.txt')

    # add "book" and "books" to every utterance
    for line in list(utterances):
        utterances.insert(0, line + " book")
        utterances.insert(0, line + " books")

    # tells how many characters needs to be dropped before the subject starts
    to_drop = 0

    for line in utterances:
        if text.startswith(line):
            to_drop = len(line)
            break

    # drops the characters and makes a list from the strings that are left
    text = text[to_drop:].strip()
    text_list = text.split(' ', len(text))

    subject_list = []
    keywords = ["books", "book", "by", "published", "written"]
    keyword = ""

    # Find out when the book name ends
    for word in text_list:
        if word not in keywords:
            subject_list.append(word)
        else:
            break

    subject = " ".join(subject_list)

    # Get all the keywords in the middle, so they can be
    # all be dropped at once, eg written by, books by
    text_list = text_list[len(subject_list):]
    if text_list:
        word = text_list[0]
        while word in keywords:
            keyword += word + " "
            text_list = text_list[1:]
            if text_list:
                word = text_list[0]
            else:
                break

    # search for an author from the rest of the characters
    author_text = text[len(keyword):].strip()
    author = AS.search(author_text, False)
    if author is "":
        author = None

    # There might be old info in the extra_info (author), so 
    # we need to clear it
    extra_info.clear()

    # add the author to extra info so it can be used in the Finna API call
    if author:
        extra_info += ["author:\"" + author + "\""]
    elif intent['sessionAttributes'].get('author'):
        extra_info += [
            "author:\"" + intent['sessionAttributes']['author'] + "\""
        ]

    # The Finna API call
    request = lookfor(term=subject, filter=extra_info)['json']

    return parse_subject(request, subject, {'author': author})


def extra_info(intent):
    """
    :param intent: Input from AWS servers
    :return: Response to AWS server in JSON format
    """
    subject = intent['sessionAttributes']['subject']
    author = intent['sessionAttributes'].get('author')
    slots = intent['currentIntent']['slots']

    lower = 0
    upper = 9999

    slot_lower = slots.get('lower')
    slot_upper = slots.get('upper')
    slot_year = slots.get('year')

    # Find out if there is a publish year in intent's slots'
    if slot_lower or slot_upper or slot_year:
        if slot_lower:
            lower = slot_lower
        if slot_upper:
            upper = slot_upper
        if slot_year:
            lower = slot_year
            upper = slot_year

        """
        Add publication year range to extra info so it can be used in the 
        Finna API. Default is from 0 to 9999.
        """
        date = "search_daterange_mv:\"[" + str(lower) + " TO " + str(
            upper) + "]\""
        extra_info = [date]

        # The Finna API call and update of session attributes
        request = lookfor(term=subject, filter=extra_info)['json']
        session_attributes = {'lower': lower, 'upper': upper, 'author': author}

        return parse_subject(request, subject, session_attributes)
    else:
        # If there's no publication year in slots, search for author
        return author_search(intent, subject)


def author_search(intent, subject):

    author = AS.search(intent['inputTranscript'])

    # If author is found, make an API call with it.
    if author:
        request = lookfor(subject, filter=["author:\"" + author + "\""])['json']
        return parse_subject(request, subject, {'author': author})

    return util.elicit_intent({'subject': subject, 'author': author},
                              "No extra information was given.")


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

    return {'status_code': r.status_code, 'json': r.json()}


def timeout_handler(signum, frame):  # pragma: no cover
    raise RuntimeError('Timed out!')


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
    
    signal.signal(signal.SIGALRM, timeout_handler)
    # Allow 4 seconds to get a response back from finna api
    signal.alarm(4)

    sess = requests.Session()
    sess.headers.update(__headers)
    sess.params.update(params)

    r = sess.request(url=__url + 'search', method=method)
    sess.close()

    signal.alarm(0)

    res = {'status_code': r.status_code, 'json': r.json()}
    return res
