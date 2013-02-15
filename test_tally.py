from tally import Tally
import unittest

class TestTally(unittest.TestCase):

    def setUp(self):
        pass

    def one_tally(self):
        return Tally(global_key_length=1, global_max_key_length=1)

    def two_tally(self):
        return Tally(global_key_length=1, global_max_key_length=2)

    def test_new_key_is_right_length(self):
        tally = Tally()
        self.assertEqual(len(tally.new_key()), tally.key_length)

    def test_new_key_is_unique(self):
        tally = Tally()
        key1 = tally.new_key()
        key2 = tally.new_key()
        self.assertNotEqual(key1, key2)

    def test_all_keys_are_unique_one(self):
        tally = self.one_tally()
        keys = {}
        for i in range(26):
            key = tally.new_key()
            self.assertTrue(key not in keys)
            keys[key] = True

    def test_all_keys_are_unique_two(self):
        tally = self.two_tally()
        keys = {}
        for i in range(26*26 + 26):
            key = tally.new_key()
            self.assertTrue(key not in keys)
            keys[key] = True

    def test_out_of_keys_one(self):
        tally = self.one_tally()
        for i in range(26):
            key = tally.new_key()
        self.assertRaises(Tally.OutOfKeysError, tally.new_key)

    def test_out_of_keys_two(self):
        tally = self.two_tally()
        for i in range(26*26 + 26):
            tally.new_key()
        self.assertRaises(Tally.OutOfKeysError, tally.new_key)

if __name__ == '__main__':
    unittest.main()
