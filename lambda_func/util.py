import json
# --------------- Helpers that build all of the responses ---------------------


def close(session_attributes, fulfillment_state, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }


"""
NOT NEEDED YET
def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        "dialogAction": {
            "type": "Delegate",
            "slots": slots
        }
    }

"""

# TBD def confirmIntent():


def elicit_intent(session_attributes, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }


"""
NOT NEEDED YET
def elicit_slot(session_attributes, message, slots, intent_name, slot_name):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'message': {
                'contentType': 'PlainText',
                'content': message
            },
            'slots': slots,
            'intentName': intent_name,
            'slotToElicit': slot_name
        }
    }
"""


def handle_session_end_request():
    message = "Hope you found what you were looking for"
    return close({}, 'Fulfilled', message)


def debug(event):
    response = {
        'sessionAttributes': {},
        'dialogAction': {
            'type': 'ElicitIntent',
            'message': {
                'contentType': 'PlainText',
                'content': json.dumps(event)
            }
        }
    }
    return response


"""
Takes list of strings as a parameter and parses it's elements to sound better
in Libby's speech. For example: 4.50 -> 4 euros 50 cents  and 4.00 -> 4 euros
"""


def parse_prices(prices):
    res = []
    for s in prices:
        price = list(s)
        if s[2] == '0':
            s = s[0]
            res.append(s + " euros")
        elif is_number(s):
            for i in range(0, len(price)):
                if price[i] == '.':
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


def make_string_list(list):
    if len(list) > 1:
        ordered_list = sorted(list)
        last = ordered_list.pop()
        return ", ".join(ordered_list) + " and " + last
    else:
        return list[0]
