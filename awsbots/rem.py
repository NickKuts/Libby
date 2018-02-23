from bot_factory import BotFactory

b = BotFactory()
n = b.load_bot_from_file('bots/libby1.json')['name']
r = b.remove_bot(n)
