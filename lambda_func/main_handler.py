from router import Router

# --------------- Main handler ------------------


def lambda_handler(event, context):
    intent = event['intentName']
    router = Router(intent)
    return router.route()
