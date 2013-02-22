import unittest

from tally.tally import Tally, Tallies

class TestTally(unittest.TestCase):

    def setUp(self):
        pass

    def test_new_counter_is_zero(self):
        tally = Tally()
        value = tally.value
        self.assertEqual(value, 0)

    def test_key_not_found_get(self):
        tallies = Tallies()
        self.assertRaises(KeyError, tallies.get, 't')

    def test_new_key_is_unique(self):
        tally1 = Tally()
        tally2 = Tally()
        self.assertNotEqual(tally1.key, tally2.key)

    def test_many_keys_are_unique_one(self):
        keys = {}
        for i in range(451):
            key = Tally().key
            self.assertTrue(key not in keys)
            keys[key] = True

    def test_increment(self):
        tally = Tally()
        tally.inc()
        self.assertEqual(tally.value, 1)

        tally.inc(inc=2)
        self.assertEqual(tally.value, 3)

    def test_decrement(self):
        tally = Tally()

        tally.inc(inc=-1)
        self.assertEqual(tally.value, -1)

        tally.inc(inc=-2)
        self.assertEqual(tally.value, -3)

    def test_setting_initial_sets_value(self):
        tally = Tally()

        tally.initial = 3

        self.assertEqual(tally.initial, 3)
        self.assertEqual(tally.value, 3)

if __name__ == '__main__':
    unittest.main()
