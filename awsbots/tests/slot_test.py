import unittest
import boto3
from slot_factory import SlotFactory

class TestSlotFactory(unittest.TestCase):
    s = SlotFactory() 
    test_all = False

    def test_save(self):
        ret = self.s.save_slot('Categories')
        assert(ret is not None)
        assert(ret['name'] == 'Categories')

    def test_get(self):
        ret = self.s.get_slot('Categories')
        assert(ret is not None)
        assert(ret['name'] == 'Categories')

    def test_load(self):
        ret = self.s.load_slot_from_file('slots/categories1.json')
        assert(ret is not None)

    def test_create_update_remove(self):
        if self.test_all:
            ret1 = self.s.create_slot('slots/categories1.json')
            assert(ret1 is not None)
            
            #There is a progress still ongoing
            time.sleep(10)
            ret2 = self.s.update_slot('slots/categories1.json')
            assert(ret2 is not None)

            #There is a progress still ongoing
            time.sleep(60)
            name = self.s.load_slot_from_file('slots/categories1.json')['name']
            ret3 = self.s.remove_slot(name)
            assert(ret3 is not None)


def main():
    print("Main function")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilHelp)
    unittest.TextTestRunner(verbosity=2).run(suite)

