# How to use
BotFactory, IntentFactory and SlotFactory can be used to create, update and
save bots, intents and slots. Thus the work practice that is recommended is
that you get the (for example) intent that you wish to modify and save it by
using IntentFactory save() -method. Then you create a copy of it and edit it.
Then you use IntentFactory update() -method and give it the file that you
edited. It might take some time for the updates to show. 

BotFactory and SlotFactory can be used the same way.

## Methods available:
save_bot(name)
- Gets the bot from AWS and saves it to a file.

get_bot(name, process_behavior='BUILD')
- Gets the bot from AWS and returns it as a python dict.

update_bot(name, process_behavior='BUILD')
- Loads the bot from 'name' and then based on the name of bot in the file,
  updates the bot in AWS to match the file. 

load_bot_from_file(name)
- Loads the bot from 'name' file and returns it as a python dict.

create_bot(name, process_behavior='BUILD')
- Create a new bot based on a file.

remove_bot(name)
- Remove bot 'name'.

SlotFactory and IntentFactory have same methods, just replace 'bot' with 'slot'
or 'intent'.

## Examples

```
from intent_factory import IntentFactory

#Save intent 'Weather' and update it 
i = IntentFactory()
i.save_intent('Weather')
i.update_intent('intents/weather_12.json')


b = BotFactory()
bot = load_bot_from_file('bots/Libby1.json')

```


## Exceptions

BadRequestException:
- When creating a new bot, if you specify a checksum then this error will
  thrown. Example:
botocore.errorfactory.BadRequestException: An error occurred (BadRequestException) when calling the PutBot operation: checksum must be specified in PUT API, when the resource already exists

botocore.errorfactory.BadRequestException: An error occurred
(BadRequestException) when calling the PutBot operation: RelativeId does not
match Lex ARN format: bot:LibbyFromPython2:$LATEST
- The name of bots, intents or slots cannot contain numbers.



