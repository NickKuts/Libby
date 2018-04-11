from router import Router
import util
# --------------- Main handler ------------------


def lambda_handler(event, context):
    debug = False
    if debug:
        return util.debug(event)
    try:
        router = Router(event)
        return router.route()
    except:
        return util.elicit_intent({}, 'Sorry, something seemed to go wrong.')
