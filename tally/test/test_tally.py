import unittest

from tally.tally import Tally, OutOfKeysError

class TestTally(unittest.TestCase):

    def setUp(self):
        pass

    def test_new_counter_is_zero(self):
        tally = Tally()
        key = tally.new_key()
        value = tally.get(key)
        self.assertEqual(value, 0)

    def test_key_not_found_get(self):
        tally = Tally()
        self.assertRaises(KeyError, tally.get, 't')

    def test_key_not_found_inc(self):
        tally = Tally()
        self.assertRaises(KeyError, tally.inc, 't')

    def test_new_key_is_unique(self):
        tally = Tally()
        key1 = tally.new_key()
        key2 = tally.new_key()
        self.assertNotEqual(key1, key2)

    def test_many_keys_are_unique_one(self):
        tally = Tally()
        keys = {}
        for i in range(26):
            key = tally.new_key()
            self.assertTrue(key not in keys)
            keys[key] = True

    def test_increment(self):
        tally = Tally()
        key = tally.new_key()

        tally.inc(key)
        new_value = tally.get(key)
        self.assertEqual(new_value, 1)

        tally.inc(key, inc=2)
        new_value = tally.get(key)
        self.assertEqual(new_value, 3)

    def test_decrement(self):
        tally = Tally()
        key = tally.new_key()

        tally.inc(key, inc=-1)
        new_value = tally.get(key)
        self.assertEqual(new_value, -1)

        tally.inc(key, inc=-2)
        new_value = tally.get(key)
        self.assertEqual(new_value, -3)

if __name__ == '__main__':
    unittest.main()
