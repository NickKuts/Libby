import util
import robertscoffee
import weather

class Router():
# --------------- Functions that control the skill's behavior ------------------
    def __init__(self, intent):
        print(intent['name'])
        self.intent = {"name": "Locate","slots": {"restaurant": {"name": "restaurant","value": "Roberts coffee"}}}
        self.intents = {"Roberts_Coffee": robertscoffee.menu_handler,
                        "Locate": self.locate,
                        "Get_Weather": weather.weather_handler,
                        "AMAZON.HelpIntent": self.get_welcome_response,
                        "AMAZON.StopIntent": self.handle_session_end_request,
                        "AMAZON.CancelIntent": self.handle_session_end_request}
    
    def locate(self):
        print("tomi on paras jeejejej4jej----------------------------------")
        restaurants = {"Roberts coffee": "in first floor of learning center", "tomi": "jeejee"}
        
        name = self.intent['slots']['restaurant']['value']
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
        speech_output = "Welcome to the restaurant helper. "
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
               
    def route(self):
        return self.intents[self.intent['name']]

