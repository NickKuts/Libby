import unittest
import boto3
from bot_factory import BotFactory
import time

class TestBotFactory(unittest.TestCase):
    b = BotFactory() 
    test_all = False

    def test_save(self):
        ret = self.b.save_bot('Libby')
        assert(ret is not None)
        assert(ret['name'] == 'Libby')

    def test_get(self):
        ret = self.b.get_bot('Libby')
        assert(ret is not None)
        assert(ret['name'] == 'Libby')

    def test_load(self):
        ret = self.b.load_bot_from_file('bots/libby1.json')
        assert(ret is not None)

    def test_create_update_remove(self):
        if self.test_all:
            ret1 = self.b.create_bot('bots/libby1.json')
            assert(ret1 is not None)
            
            #There is a progress still ongoing
            time.sleep(10)
            ret2 = self.b.update_bot('bots/libby1.json')
            assert(ret2 is not None)

            #There is a progress still ongoing
            time.sleep(60)
            name = self.b.load_bot_from_file('bots/libby1.json')['name']
            ret3 = self.b.remove_bot(name)
            assert(ret3 is not None)

def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilHelp)
    unittest.TextTestRunner(verbosity=2).run(suite)

