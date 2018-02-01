from intent_factory import IntentFactory

i = IntentFactory()

name = 'Weather'
fname = 'intents/w2.json'
i.create_intent(fname)
# i.update_intent('Weather')
# i.save_intent(name)
