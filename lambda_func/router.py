import util
import robertscoffee
import weather

"""
This class takes intent as a parameter and finds what Alexa should answer. To add an intent, add the name of the intent 
you want to add as a key and it's method as a value in the self.intents dictionary. If method added needs some values as
parameter, you should add it in the else-if chain in the route method(last method in this class).  
"""


class Router():
    def __init__(self, intent):
        print(intent['name'])
        self.intent = intent
        self.intents = {"RC_Intro": robertscoffee.intro,
                        "Get_Prices": robertscoffee.prices,
                        "Get_Drinks": robertscoffee.drinks,
                        "Locate": self.locate,
                        "Get_Weather": weather.weather_handler,
                        "Unhandled": self.unhandled_request,
                        "AMAZON.HelpIntent": self.get_welcome_response,
                        "AMAZON.StopIntent": self.handle_session_end_request,
                        "AMAZON.CancelIntent": self.handle_session_end_request}
    """
    Function which tells user the location of restaurant/coffeehouse (s)he is looking for. To add a location, add
    name of the place you want to add as a key and it's location as a value in the restaurants dictionary.
    """
    def locate(self):
        print("Locate method")
        restaurants = {"roberts coffee": "in the first floor of the learning center"}
        name = self.intent['slots']['restaurant']['value'].lower()
        card_title = "Locate"
        speech_output = "%s is located %s"%(name, restaurants[name])
        # Setting this to true ends the session and exits the skill.
        should_end_session = False
        return util.build_response({}, util.build_speechlet_response(
            card_title, speech_output, None, should_end_session))

               
    def get_welcome_response(self):
        """ If we wanted to initialize the session to have some attributes we could
        add those here
        """
    
        session_attributes = {}
        card_title = "Welcome"
        speech_output = "Hi! I'm Libby and I'm here to help you choose what you want to order from Robert's Coffee or" \
                        " to know what kind of weather there is outside. Start by asking about the weather or Robert's" \
                        "Coffee."

        # If the user either does not reply to the welcome message or says something
        # that is not understood, they will be prompted again with this text.
        reprompt_text = "Say something"
        should_end_session = False
        return util.build_response(session_attributes, util.build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    
    def unhandled_request(self):
        card_title = "Unhandled"
        speech_output = "Sorry I don't know that one."
        # Setting this to true ends the session and exits the skill.
        should_end_session = False
        return util.build_response({}, util.build_speechlet_response(
            card_title, speech_output, None, should_end_session))
    
    def handle_session_end_request(self):
        card_title = "Session Ended"
        speech_output = "Hope you found what you were looking for"
        # Setting this to true ends the session and exits the skill.
        should_end_session = True
        return util.build_response({}, util.build_speechlet_response(
            card_title, speech_output, None, should_end_session))

    """
    This is where the magic happens. If a method needs for example the intent as a parameter (for getting the 
    user's input) add it in the if-chain. If it doesn't need parameters add it only in self.intents dictionary.
    """

    def route(self):
        name = self.intent['name']
        if name == "Get_Drinks":
            return self.intents[name](self.intent['slots']['category']['value'])
        if name == "Get_Prices":
            return self.intents[name](self.intent)    
        return self.intents[name]()

