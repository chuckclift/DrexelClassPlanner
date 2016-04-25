import unittest
from resolveClasses import *
from collections import namedtuple



# def get_start_time(time_string):
# def get_end_time(time_string):
# def class_time_overlap(start1, end1, start2, end2):
# def get_class_type(class_info):
# def time_overlap(class1, class2):
# def valid_combo(classes):
# def get_valid_schedules(target_classes, class_schedule):
# def read_data(datafile):
# def generate_schedules(data_file, target_classes):
# def print_plan(title, classes):
# def report(data_file, target_classes, title):

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

    def test_get_class_type(self):
        course = namedtuple('course', ['name', 'instr_type', 'instr_method', 'crn', 'day_time'])
        class1 = course("entp 100", "lecture", "Face to Face", "14198", "W  10:00 am - 10:50 am")

        self.assertEqual("entp 100 lecture", get_class_type(class1))
        self.assertFalse("foo 101 lecture" == get_class_type(class1))


        



if __name__ == "__main__":
    unittest.main()
