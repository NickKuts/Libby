from bot_factory import BotFactory

b = BotFactory()
fname = 'bots/libby1.json'
name = 'LibbyFromPython'
r = b.update_bot(fname)

#r = b.update_bot('Libby')
#ret = b.create_bot(fname)
#bot = b.save_bot('Libby')
