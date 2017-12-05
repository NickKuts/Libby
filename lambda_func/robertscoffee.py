import util
import json

data = json.load(open('robertscoffee.json'))

def menu_handler():
    card_title = "Restaurant menu"
    speech_output = "Go to Robert's Coffee for coffee"
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return util.build_response({}, util.build_speechlet_response(
        card_title, speech_output, None, should_end_session))