import get_weather
import util


def weather_handler():
    # update_data()
    data = get_weather.read_data()
    
    # card_title = "Weather in otaniemi"
    message = {
        'contentType': 'PlaintText',
        'content': "The temperature is around " + str(data[0])
    }
    return util.close({}, 'Fulfilled', message)
