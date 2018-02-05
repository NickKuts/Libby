import boto3
import json


class IntentFactory:

    def __init__(self):
        self.client = boto3.client('lex-models')
        self.lambda_client = boto3.client('lambda')

    def load_intent_from_file(self, name):
        data = {}

        with open(name, 'r') as f:
            d = f.read()
            data = json.loads(d)
        return data

    def update_intent(self, name):
        
        data = self.load_intent_from_file(name)

        try:
            data.pop('lastUpdatedDate', None)
            data.pop('createdDate', None)
            data.pop('version', None)
        except:
            print("Failed to remove parts from json")

        res = self.client.put_intent(**data)

    def create_intent(self, fname):
       
        data = self.load_intent_from_file(fname)
        name = data['name']
        
        try:
            data.pop('ResponseMetadata', None)
            data.pop('lastUpdatedDate', None)
            data.pop('createdDate', None)
            data.pop('version', None)
        except Exception as e:
            print("no data to remove from json data")
            print(e)

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
