import boto3
import json
from datetime import datetime


class BotFactory():
    def __init__(self):
        self.client = boto3.client('lex-models')

    def save_bot(self, name):
        bot = self.get_bot(name)
        bot['lastUpdatedDate'] = str(bot['lastUpdatedDate'])
        bot['createdDate'] = str(bot['createdDate'])
        d = bot['lastUpdatedDate'][:16].replace(" ", "_")
        v = bot['version']
        # e.g. Libby_dev-2018-01-3016:30
        fname = "bots/" + name + "-" + d + ".json"
        data = json.dumps(bot)
        with open(fname, 'w') as f:
            f.write(data)

    def get_bot(self, name, version='$LATEST'):
        response = self.client.get_bot(
            name=name,
            versionOrAlias=version
        )
        return response

    def update_bot_from_data(self, bot_data, process_behavior):
        name = bot_data['name']
        print("Bot name",name)
        try:
            description = bot_data['description']
        except:
            description = "A bot."
            print("No description found for bot, creating it.")

        intents = bot_data['intents']
        clarification_prompt = bot_data['clarificationPrompt']
        abort_statement = bot_data['abortStatement']
        idleSessionTTLInSeconds = bot_data['idleSessionTTLInSeconds']
        voiceId = bot_data['voiceId']
        checksum = bot_data['checksum']
        locale = bot_data['locale']
        child_directed = bot_data['childDirected']
        
        if checksum == "":
            response = self.client.put_bot(
                name=name,
                description=description,
                intents=intents,
                clarificationPrompt=clarification_prompt,
                abortStatement=abort_statement,
                idleSessionTTLInSeconds=idleSessionTTLInSeconds,
                voiceId=voiceId,
                processBehavior=process_behavior,
                locale=locale,
                childDirected=child_directed
            )
        else:
            response = self.client.put_bot(
                name=name,
                description=description,
                intents=intents,
                clarificationPrompt=clarification_prompt,
                abortStatement=abort_statement,
                idleSessionTTLInSeconds=idleSessionTTLInSeconds,
                voiceId=voiceId,
                checksum=checksum,
                processBehavior=process_behavior,
                locale=locale,
                childDirected=child_directed
            )   
        return response

    def update_bot(self, name, process_behavior='BUILD'):
        # bot_data = self.get_bot(name)
        bot_data = self.load_bot_from_file(name) 
        res = self.update_bot_from_data(bot_data, process_behavior)

    def load_bot_from_file(self, name):
        bot_data = {}
        with open(name, 'r') as f:
            d = f.read()
            bot_data = json.loads(d)
        return bot_data

    def create_bot(self, name, process_behavior='BUILD'):
        bot_data = self.load_bot_from_file(name)
        bot_data['checksum'] = ""
        res = self.update_bot_from_data(bot_data, process_behavior)

