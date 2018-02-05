import util
import robertscoffee
import weather
import get_help

"""
This class takes intent as a parameter and finds what Libby should answer.
To add an intent, add the name of the intent you want to add as a key and
it's method as a value in the self.intents dictionary. If method added needs
some values as parameter, you should add it in the else-if chain in the route
method(last method in this class).
"""


class Router:
    def __init__(self, intent):
        # print(intent['name'])
        self.intent = intent
        self.intents = {"Get_Categories": robertscoffee.intro,
                        "Get_Prices": robertscoffee.prices,
                        "Get_Drinks": robertscoffee.drinks,
                        "Weather": weather.weather_handler,
                        "Get_Help": get_help.help_answer,
                        "Thanks": util.handle_session_end_request
                        }
    """
    This is where the magic happens. If a method needs for example the intent
    as a parameter (for getting the user's input) add it in the if-chain. If
    it doesn't need parameters add it only in self.intents dictionary.
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
