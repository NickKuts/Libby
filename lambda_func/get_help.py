from . import util
import json

"""
help_answer return the help answer depend which help is asking. If user use only word "help" the answer is the 
basic Libby answer other way the answer is from the "help.json" -file. Where is all the help which are useful. 
"""
def help_answer(intent):
    null = None
    if intent['slots']['what'] == null:
        message = {
            'contentType': 'PlainText',
            'content': "Hi! I'm Libby help. Get more help ask weather help or roberts coffee menu asking categories."

        }
        return util.elicit_intent({}, message)

    else:
        data = json.load(open('help.json'))
        name = intent['slots']['what'].lower
        message = {
            'contentType': 'PlainText',
            'content': data[name]
        }
        return util.elicit_intent({}, message)

