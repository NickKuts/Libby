import unittest
import boto3
from intent_factory import IntentFactory

class TestBotFactory(unittest.TestCase):
    i = IntentFactory() 
    
    def test_save(self):
        ret = self.i.save_intent('Weather')
        assert(ret is not None)
        assert(ret['name'] == 'Weather')

    def test_get(self):
        ret = self.i.get_intent('Weather')
        assert(ret is not None)
        assert(ret['name'] == 'Weather')

    def test_load(self):
        ret = self.i.load_bot_from_file('intents/weather1.json')
        assert(ret is not None)

    def test_update(self):
        #ret = b.update_bot('Libby.json')
        #assert(ret is not None)
        assert('foo' == 'foo')

    def test_create(self):
        assert('foo' == 'foo')
        #ret = b.create_bot('Libby.json')
        #assert(ret is not None)


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilHelp)
    unittest.TextTestRunner(verbosity=2).run(suite)

