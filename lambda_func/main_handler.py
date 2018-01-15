from router import Router
import util
# --------------- Main handler ------------------


def lambda_handler(event, context):
    debug = False
    if debug:
        return util.debug(event)
    print(context)
    intent = event['currentIntent']
    router = Router(intent)
    return router.route()
