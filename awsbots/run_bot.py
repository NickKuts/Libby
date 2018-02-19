from bot_factory import BotFactory

b = BotFactory()


n = b.load_bot_from_file('bots/libby1.json')['name']
print(n)

bot = b.get_bot(n)

print("joo")

try:
    ret = b.create_bot('bots/libby1.json')
except:
    print("bot exists alrdy")

r = b.remove_bot(n)
