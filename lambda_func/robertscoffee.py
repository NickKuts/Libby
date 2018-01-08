from . import util
import json
"""
This document includes all the methods related in Robert's Coffee. The methods take their information from the
pre-written json document robertscoffee.json.
"""

data = json.load(open('robertscoffee.json'))

category = {}

"""
Intro guides the user and tells what categories there are to choose from.
"""


def intro():
    card_title = "Introduction"
    key, value = data.popitem()
    output = ", ".join(data) + " and " + key
    data.update({key: value})
    message = {
        'contentType': 'PlainText',
        'content': "Robert's Coffee's drinkcategories are " + output
    }
    reprompt_text = "You can ask more about these categories or straight about some drink. " + message['content']
    return util.elicitIntent({}, message)

"""
Categories tells the user about drinks in a selected category(user input) and returns them as like a native
englishspeaker would say them.
"""


def drinks(which):
    category = data[which]
    key, value = category.popitem()
    output = ", ".join(category) + " and " + key
    category.update({key: value})
    card_title = "Categories"
    message = {
        'contentType': 'PlainText',
        'content': which.lower() + " include " + output + ". You can ask more about these drinks or about any other category or drink."
    }
    slots = {

    }
    reprompt_text = message + "You can also ask help anytime you want."
    return util.elicitIntent({}, message)

"""
Prices tells prices for all of the sizes the drink is possible to buy.
"""


def prices(intent):
    drink = intent['slots']['consumable'].lower()
    drinks = {}
    for i in data.values():
        drinks.update(i)
    sizes = util.parse_prices(list(sum(sorted(drinks[drink]['size'].items(), key=lambda x: x[1]), ())))

    key, value = sizes[len(sizes) - 2], sizes[len(sizes) - 1]
    sizes = sizes[0: len(sizes) - 2]
    output = ""
    if len(sizes) > 0:
        output += ", ".join(sizes) + " and "
    output += key + ", " + value
    card_title = "Drink"
    message = {
        'contentType': 'PlainText',
        'content': "Prices for " + drink + " are: " + output
    }
    reprompt_text = message['content'] + ". You can ask about a different drink or thank me if you want to end the converstation."
    return util.elicitIntent({}, message)
