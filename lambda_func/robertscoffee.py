import util
import json
"""
This document includes all the methods related in Robert's Coffee. The methods take their information from the 
pre-written json document robertscoffee.json.
"""

data = json.load(open('robertscoffee.json'))

"""
Intro guides the user and tells what categories there are to choose from.
"""


def intro():
    # card_title = "Introduction"
    key, value = data.popitem()
    output = ", ".join(data) + " and " + key
    data.update({key: value})
    message = {
        'contentType': 'PlainText',
        'content': "Robert's Coffee's drinkcategories are " + output
    }
    return util.elicit_intent({}, message)


"""
Categories tells the user about drinks in a selected category(user input) and returns them as like a native 
english speaker would say them.
"""


def drinks(which):
    category = data[which]
    key, value = category.popitem()
    output = ", ".join(category) + " and " + key
    category.update({key: value})
    # card_title = "Categories"
    message = {
        'contentType': 'PlainText',
        'content': which.lower() + " include " + output + ". You can ask more about these drinks or about any other "
                                                          "category or drink."
    }
    """
    slots = {

    }
    """
    return util.elicit_intent({}, message)


"""
Prices tells prices for all of the sizes the drink is possible to buy. 
"""


def prices(intent):
    drink = intent['slots']['consumable'].lower()
    consumables = {}
    for i in data.values():
        consumables.update(i)
    sizes = util.parse_prices(list(sum(sorted(consumables[drink]['size'].items(), key=lambda x: x[1]), ())))

    key, value = sizes[len(sizes) - 2], sizes[len(sizes) - 1]
    sizes = sizes[0: len(sizes) - 2]
    output = ""
    if len(sizes) > 0:
        output += ", ".join(sizes) + " and "
    output += key + ", " + value
    # card_title = "Drink"
    message = {
        'contentType': 'PlainText',
        'content': "Prices for " + drink + " are: " + output
    }
    return util.elicit_intent({}, message)
