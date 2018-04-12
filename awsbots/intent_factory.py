import boto3
import json
import time
import random

class IntentFactory:

    def __init__(self):
        self.client = boto3.client('lex-models')
        self.lambda_client = boto3.client('lambda')

    def load_intent_from_file(self, fname):
        data = {}

        with open(fname, 'r') as f:
            d = f.read()
            data = json.loads(d)
        return data

    def update_intent(self, name):
 
        data = self.load_intent_from_file(name)
        old_data = self.get_intent(data['name'])
        data['checksum'] = old_data['checksum']

        arr = ['ResponseMetadata', 'lastUpdatedDate', 'createdDate', 'version']

        for key in arr:
            try:
                data.pop(key)
            except:
                print("No key '"+key+"' to remove")

        res = self.client.put_intent(**data)
        print('Successfully updated intent', data['name'])
        return res

    def create_intent(self, fname):
 
        data = self.load_intent_from_file(fname)
        dummy = self.load_intent_from_file('intents/dummy.json')
        name = data['name']
        
        dummy['name'] = name
        
        arr = ['ResponseMetadata','lastUpdatedDate', 
                'createdDate','version']
        
        for key in arr:
            try:
                data.pop(key)
            except:
                print("No key '"+key+"' to remove")
        
        res = self.client.put_intent(**dummy)
        time.sleep(5)

        intent = self.get_intent(name)
        data['checksum'] = intent['checksum']

        lambda_res = self.lambda_client.add_permission(
            FunctionName='Libby',
            StatementId=str(random.randint(0, 100000)),
            Action='lambda:*',
            Principal='lex.amazonaws.com',

        )

        real_res = self.client.put_intent(**data)
        print("Successfully created intent", name)
        return real_res

    def get_intent(self, name, version='$LATEST'):
        response = self.client.get_intent(
            name=name,
            version=version
        )
        return response

    def save_intent(self, name, version='$LATEST'):
        intent = self.get_intent(name, version)

        intent['lastUpdatedDate'] = str(intent['lastUpdatedDate'])
        intent['createdDate'] = str(intent['createdDate'])
        d = intent['lastUpdatedDate'][:16].replace(" ", "_")
        fname = "intents/" + name + "-" + d + ".json"
        data = json.dumps(intent)
        with open(fname, 'w') as f:
            f.write(data)
            print("Successfully saved intent", name)
        
        return intent

    def remove_intent(self, name):
        response = self.client.delete_intent(
            name=name
        )
        print("Successfully removed intent", name)
        return response
