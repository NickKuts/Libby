from router import Router

# --------------- Main handler ------------------


def lambda_handler(event):
    intent = event['intentName']
    router = Router(intent)
    return router.route()
