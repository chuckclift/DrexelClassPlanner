import unittest
from resolveClasses import *

class MyTest(unittest.TestCase):
    def test_get_start_time(self):
        time_string = "R 01:00 pm - 03:50 pm"
        self.assertEqual(1300, get_start_time(time_string))

    def test_get_end_time(self):
        time_string = "R 01:00 pm - 03:50 pm"
        self.assertEqual(1550, get_end_time(time_string))

    def test_class_time_overlap(self):
        self.assertFalse(class_time_overlap(0, 100, 1200, 1300))
        self.assertTrue(class_time_overlap(1130, 1230, 1200, 1300))



if __name__ == "__main__":
    unittest.main()
