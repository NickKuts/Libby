from router import Router
import util
# --------------- Main handler ------------------


def lambda_handler(event, context):
    debug = False
    if debug:
        return util.debug(event)

    # intent = event['currentIntent']
    router = Router(event)
    
    error_message = {'sessionAttributes': {'author': None}, 
                     'dialogAction': 
                        {'type': 'ElicitIntent', 
                         'message': {
                            'contentType': 'PlainText', 
                            'content': "I'm sorry. I'm having connection issues."}
                        }
                    }

    try:
        res = router.route()
        print("at main handler")
        print(res)
        return res
    except RuntimeError:
        return error_message
    except Exception as e:
        error_message['dialogAction']['message']['content'] = "I'm sorry, I cannot answer that. Error was " + str(e)
        return error_message
