import boto3
import json


class IntentFactory:

    def __init__(self):
        self.client = boto3.client('lex-models')

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

        arr = ['lastUpdatedDate', 'createdDate', 'version']

        for key in arr:
            try:
                data.pop(key)
            except:
                print("No key '"+key+"' to remove")

        res = self.client.put_intent(**data)

    def create_intent(self, fname):
 
        data = self.load_intent_from_file(fname)
        name = data['name']
        
        arr = ['ResponseMetadata','lastUpdatedDate', 
                'createdDate','version']
        
        for key in arr:
            try:
                data.pop(key)
            except:
                print("No key '"+key+"' to remove")

        real_res = self.client.put_intent(**data)

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
        
        return intent

    def remove_intent(self, name):
        response = self.client.delete_intent(
            name=name
        )
        return response
