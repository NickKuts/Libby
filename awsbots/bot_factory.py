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

    def update_bot(self, name, process_behavior='BUILD'):
        bot_data = self.load_bot_from_file(name)
        old_data = self.get_bot(bot_data['name'])
        bot_data['checksum'] = old_data['checksum']

        try:
            bot_data.pop('ResponseMetadata')
            bot_data.pop('status')
            bot_data.pop('lastUpdatedDate')
            bot_data.pop('createdDate')
            bot_data.pop('version')
        except:
            print("Failed to pop all from bot data")


        res = self.client.put_bot(**bot_data)

    def load_bot_from_file(self, name):
        bot_data = {}
        with open(name, 'r') as f:
            d = f.read()
            bot_data = json.loads(d)
        return bot_data

    def create_bot(self, name, process_behavior='BUILD'):
        bot_data = self.load_bot_from_file(name)
        
        try:
            bot_data.pop('checksum')
            bot_data.pop('ResponseMetadata')
            bot_data.pop('status')
            bot_data.pop('lastUpdatedDate')
            bot_data.pop('createdDate')
            bot_data.pop('version')
        except:
            print("failed to checksum")
        
        res = self.client.put_bot(**bot_data)

