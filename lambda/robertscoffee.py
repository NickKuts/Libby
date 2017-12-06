import util
import json

data = json.load(open('robertscoffee.json'))

category = {}

def menu_handler():
    card_title = "Restaurant menu"
    speech_output = "Go to Robert's Coffee for coffee"
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return util.build_response({}, util.build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def categories(which):
    category = data[which]
    
    key, value = category.popitem()
    output = ", ".join(category) + " and " + key
    category.update({key: value})
    card_title = "Categories"
    speech_output = "We have " + output + ". You can ask more about these drinks."
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return util.build_response({}, util.build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
def drinks(intent):
    drink = intent['slots']['consumable']['value']
    drinks = {}
    for i in data.values():
        drinks.update(i)
    sizes = list(sum(sorted(drinks[drink]['size'].items(), key=lambda x:x[1]), ()))
    key, value = sizes[len(sizes)- 2], sizes[len(sizes) - 1]
    output = ", ".join(sizes) + " and " + key + ", " + value + " euros."
    card_title = "Drink"
    speech_output = "Prices for " + drink + " are: " + output
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return util.build_response({}, util.build_speechlet_response(
        card_title, speech_output, None, should_end_session))
