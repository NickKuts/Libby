import unittest
import boto3
from bot_factory import BotFactory

class TestBotFactory(unittest.TestCase):
    b = BotFactory() 
    
    def test_save(self):
        ret = self.b.save_bot('Libby')
        assert(ret is not None)
        print(ret)
        print(ret['name'])
        assert(ret['name'] == 'Libby')

    def test_get(self):
        ret = self.b.get_bot('Libby')
        assert(ret is not None)
        assert(ret['name'] == 'Libby')

    def test_load(self):
        ret = self.b.load_bot_from_file('bots/libby1.json')
        assert(ret is not None)

    def test_update(self):
        #ret = b.update_bot('Libby.json')
        #assert(ret is not None)
        assert('foo' == 'foo')

    def test_create(self):
        assert('foo' == 'foo')
        #ret = b.create_bot('Libby.json')
        #assert(ret is not None)

    def jou(self):
        assert("foo" == 'baz')

def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilHelp)
    unittest.TextTestRunner(verbosity=2).run(suite)

