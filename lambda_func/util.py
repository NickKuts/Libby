
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

"""
Takes list of strings as a parameter and parses it's elements to sound better in Alexa's speech. For example: 
4.50 -> 4 euros 50 cents  and 4.00 -> 4 euros
"""
def parse_prices(prices):
    res = []
    for s in prices:
        price = list(s)
        if s[2] == '0':
            s = s[0]
            res.append(s + " euros")
        elif is_number(s):
            for i in range (0,len(price)):
                if(price[i] == '.'):
                    price[i] = ' euros '
            res.append("".join(price) + " cents")
        else:
            res.append(s)
    return res

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False