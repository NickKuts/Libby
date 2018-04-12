import unittest
import boto3
from intent_factory import IntentFactory
import time

class TestIntentFactory(unittest.TestCase):
    i = IntentFactory() 
    test_all = True
    fname = 'intents/intent_test.json'

    def test_save(self):
        ret = self.i.save_intent('Weather')
        assert(ret is not None)
        assert(ret['name'] == 'Weather')

    def test_get(self):
        ret = self.i.get_intent('Weather')
        assert(ret is not None)
        assert(ret['name'] == 'Weather')

    def test_load(self):
        ret = self.i.load_intent_from_file(self.fname)
        assert(ret is not None)

    def test_create_update_remove(self):
        if self.test_all:
            time.sleep(10)
            ret1 = self.i.create_intent(self.fname)
            assert(ret1 is not None)
            
            #There is a progress still ongoing
            time.sleep(40)
            ret2 = self.i.update_intent(self.fname)
            assert(ret2 is not None)

            #There is a progress still ongoing
            time.sleep(60)
            name = self.i.load_intent_from_file(self.fname)['name']
            ret3 = self.i.remove_intent(name)
            assert(ret3 is not None)

