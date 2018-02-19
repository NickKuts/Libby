import boto3
import json


class SlotFactory:

    def __init__(self):
        self.client = boto3.client('lex-models')

    def load_slot_from_file(self, fname):        
        data = {}

        with open(fname, 'r') as f:
            d = f.read()
            data = json.loads(d)
        return data
    
    def update_slot(self, name):

        data = self.load_slot_from_file(name) 
        old_data = self.get_slot(data['name'])
        data['checksum'] = old_data['checksum']

        arr = ['lastUpdatedDate', 'createdDate', 'version']

        for key in arr:
            try:
                bot_data.pop(key)
            except:
                print("No key '"+key+"' to remove")

        res = self.client.put_slot_type(**data)
        if res is not None:
            print("Successfully updated slot")

    def create_slot(self, fname):

        data = self.load_slot_from_file(fname)
        name = data['name']        
        arr = ['ResponseMetadata','lastUpdatedDate', 
                'createdDate','version', 'checksum']

        for key in arr:
            try:
                data.pop(key)
            except:
                print("No key '"+key+"' to remove")

        res = self.client.put_slot_type(**data)

        if res is not None:
            print("Successfully created slot")

    def get_slot(self, name, version='$LATEST'):
        response = self.client.get_slot_type(
            name=name,
            version=version
        )
        return response

    def save_slot(self, name, version='$LATEST'):
        slot = self.get_slot(name, version)

        slot['lastUpdatedDate'] = str(slot['lastUpdatedDate'])
        slot['createdDate'] = str(slot['createdDate'])
        d = slot['lastUpdatedDate'][:16].replace(" ", "_")
        fname = "slots/" + name + "-" + d + ".json"
        data = json.dumps(slot)
        with open(fname, 'w') as f:
            f.write(data)

    def remove_slot(self, name):
        response = self.client.delete_slot_type(
            name=name        
        )
        return response

