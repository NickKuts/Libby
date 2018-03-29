import util
import json

"""
help_answer return the help answer depend which help is asking. If user use
only word "help" the answer is the basic Libby answer other way the answer is
from the "help.json" -file. Where is all the help which are useful.
"""


def help_answer(intent):
    if intent['slots']['what'] is None:
        message = "Hi! I'm Libby help. You can ask about weather, roberts " \
                  "coffee menu, locations or more information about some " \
                  "book or author"
        return util.elicit_intent({}, message)
    else:
        data = json.load(open('help.json'))
        name = intent['slots']['what']
        message = data[name]
        return util.elicit_intent({}, message)
