import unittest
from threading import Event

from tally.events import on_value_changed, on_new_tally
from tally.tally import Tally

class TestTally(unittest.TestCase):

    def test_new_counter_is_zero(self):
        tally = Tally()
        value = tally.value
        self.assertEqual(value, 0)

    def test_new_key_is_unique(self):
        tally1 = Tally()
        tally2 = Tally()
        self.assertNotEqual(tally1.key, tally2.key)

    def test_many_keys_are_unique_one(self):
        keys = {}
        for i in range(9):
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
        tally = Tally(initial=3)

        self.assertEqual(tally.initial, 3)
        self.assertEqual(tally.value, 3)

    def test_publish_on_value_changed(self):
        tally = Tally()
        result = [False]

        def value_changed(tally=None):
            if tally: result[0] = True

        on_value_changed(value_changed, tally.key)

        tally.inc(1)
        self.assertEqual(result[0], True)


    def test_publish_on_new(self):
        result = [False]

        def new_tally(tally=None):
            if tally: result[0] = True

        on_new_tally(new_tally)

        tally = Tally()
        self.assertEqual(result[0], True)

if __name__ == '__main__':
    unittest.main()
