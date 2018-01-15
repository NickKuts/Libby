from . import util
from . import robertscoffee
from . import weather
from . import get_help

"""
This class takes intent as a parameter and finds what Alexa should answer. To add an intent, add the name of the intent
you want to add as a key and it's method as a value in the self.intents dictionary. If method added needs some values as
parameter, you should add it in the else-if chain in the route method(last method in this class).
"""


class Router:
    # --------------- Functions that control the skill's behavior ------------------
    def __init__(self, intent):
        print(intent['name'])
        self.intent = intent
        self.intents = {"Get_Categories": robertscoffee.intro,
                        "Get_Prices": robertscoffee.prices,
                        "Get_Drinks": robertscoffee.drinks,

                     #  "Locate": self.locate,
                        "Weather": weather.weather_handler,
                        "Get_Help": get_help.help_answer,
                        # "Unhandled": util.unhandled_request,
                        # "AMAZON.HelpIntent": util.get_welcome_response,
                        "AMAZON.StopIntent": util.handle_session_end_request,
                        "AMAZON.CancelIntent": util.handle_session_end_request}

    """
    Function which tells user the location of restaurant/coffeehouse (s)he is looking for. To add a location, add
    name of the place you want to add as a key and it's location as a value in the restaurants dictionary.
    """
    """
    def locate(self):
        restaurants = {"Roberts coffee": "in first floor of learning center"}
        name = self.intent['slots']['place']
        message = {
            'contentType': 'PlainText',
            'content': "%s is located %s" % (name, restaurants[name])
        }
        return util.close({}, "Fulfilled", message)
    """

    """
    This is where the magic happens. If a method needs for example the intent as a parameter (for getting the
    user's input) add it in the if-chain. If it doesn't need parameters add it only in self.intents dictionary.
    """

    def route(self):
        name = self.intent['name']
        if name == "Get_Drinks":
            return self.intents[name](self.intent['slots']['category'])
        if name == "Get_Prices":
            return self.intents[name](self.intent)
        if name == "Get_Help":
            return self.intents[name](self.intent)
        return self.intents[name]()
