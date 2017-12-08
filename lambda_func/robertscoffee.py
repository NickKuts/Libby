import util
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
    speech_output = "Robert's Coffee's drinkcategories are " + output
    reprompt_text = "You can ask more about these categories or straight about some drink. " + speech_output
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return util.build_response({}, util.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

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
    speech_output = which.lower() + " include " + output + ". You can ask more about these drinks or about any other category or drink."
    reprompt_text = speech_output + "You can also ask help anytime you want."
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return util.build_response({}, util.build_speechlet_response(
        card_title, speech_output, None, should_end_session))

"""
Prices tells prices for all of the sizes the drink is possible to buy. 
"""
def prices(intent):
    drink = intent['slots']['consumable']['value'].lower()
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
    speech_output = "Prices for " + drink + " are: " + output
    reprompt_text = speech_output + ". You can ask about a different drink or thank me if you want to end the converstation."
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return util.build_response({}, util.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
