import unittest
import boto3
from slot_factory import SlotFactory
import time

class TestSlotFactory(unittest.TestCase):
    s = SlotFactory() 
    test_all = True
    fname = 'slots/slot_test.json'

    def test_save(self):
        ret = self.s.save_slot('Categories')
        assert(ret is not None)
        assert(ret['name'] == 'Categories')

    def test_get(self):
        ret = self.s.get_slot('Categories')
        assert(ret is not None)
        assert(ret['name'] == 'Categories')

    def test_load(self):
        ret = self.s.load_slot_from_file(self.fname)
        assert(ret is not None)

    def test_create_update_remove(self):
        if self.test_all:
            time.sleep(15)
            ret1 = self.s.create_slot(self.fname)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("RET: ", ret1)
            print(ret1)
            assert(ret1 is not None)
            
            #There is a progress still ongoing
            time.sleep(40)
            ret2 = self.s.update_slot(self.fname)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("RET: ", ret2)
            print(ret2)
            assert(ret2 is not None)

            #There is a progress still ongoing
            time.sleep(60)
            name = self.s.load_slot_from_file(self.fname)['name']
            ret3 = self.s.remove_slot(name)
            assert(ret3 is not None)


def main():  # pragma: no cover
    print("Main function")


if __name__ == '__main__':  # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSlotFactory)
    unittest.TextTestRunner(verbosity=2).run(suite)

