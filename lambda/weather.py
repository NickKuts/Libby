import get_weather
import util

def weather_handler():
   # update_data()
    data = get_weather.read_data()
    
    card_title = "Weather in otaniemi"
    speech_output = "The temperature is around " + str(data[0])
    should_end_session = False
    return util.build_response({}, util.build_speechlet_response(
        card_title, speech_output, None, should_end_session))