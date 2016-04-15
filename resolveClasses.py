#!/usr/bin/python3

from itertools import product
from collections import namedtuple
import csv
from itertools import islice

def get_start_time(time_string):
    combined_time =  int(time_string.split()[1].replace(":", ""))

    if time_string.split()[2] == "pm":
        military_time = combined_time + 1200
    else:
        military_time = combined_time
    
    return military_time 
    
def get_end_time(time_string):
    combined_time =  int(time_string.split()[4].replace(":", ""))

    if time_string.split()[5] == "pm":
        military_time = combined_time + 1200
    else:
        military_time = combined_time
    
    return military_time 

def class_time_overlap(start1, end1, start2, end2):
    # an overlap where class1 starts before class 2
    # and ends after class2 begins
    overlap1 = start1 < start2 and start2 < end1

    # an overlap where class2 starts before class 1 
    # and ends after class1 begins
    overlap2 = start2 < start1 and start1 < end2

    same_starts = start1 == start2 
    same_ends = end1 == end2
    return overlap1 or overlap2 or same_starts or same_ends



def relevant_class(class_info, relevant_classes):
    for r in relevant_classes:
        school, course_num = r.split()

        if class_info.subject.lower() == school.lower() and class_info.course_num.lower() == course_num:
            return True

def test_combination(course_combination):
    print("everything failed")
    # for c in course_combination:


def get_class_type(class_info):
    return " ".join([class_info.subject, class_info.course_num, class_info.instr_type])

def time_overlap(class1, class2):
    timeStringOne = class1.day_time
    timeStringTwo = class2.day_time

    daySetOne = set(timeStringOne.split()[0])
    daySetTwo = set(timeStringTwo.split()[0])

    no_overlap = not daySetOne.intersection(daySetTwo)
       
    if no_overlap:
        return False

    if class1.instr_method.lower() == "online" or class2.instr_method.lower() == "online":
        return False
    
    if "tbd" in class1.day_time.lower() or "tbd" in class2.day_time.lower():
        return True

    start1 = get_start_time(timeStringOne)
    end1 = get_end_time(timeStringOne)
    start2 = get_start_time(timeStringTwo)
    end2 = get_end_time(timeStringTwo)
    
    return class_time_overlap(start1, end1, start2, end2)

def valid_combo(classes):
    for c in classes:
        current_crn = c.crn

        for o in classes:  # checking each course for conflicts
            same_class = c.crn == o.crn
            if time_overlap(c, o) and not same_class:
                return False 

    return True

def get_valid_schedules(target_classes, class_schedule):
    # example input:
    # target_classes = ["ece 201", "se 210", engr 103"]
    # class_schedule = [["CS", "161", "Lab", "Face To Face", "61", "42233", "Computer Programming II", "R 01:00 pm - 03:50 pm", "STAFF"]
    #                  ,["CS", "161", "Lab", "Face To Face", "61", "42233", "Computer Programming II", "R 01:00 pm - 03:50 pm", "STAFF"]
    #                  ,["CS", "161", "Lab", "Face To Face", "61", "42233", "Computer Programming II", "R 01:00 pm - 03:50 pm", "STAFF"]] 

    # break class schedule to relevant classes
    relevant_classes = [a for a in class_schedule if relevant_class(a, target_classes)]
    print("relevant_classes: ", len(relevant_classes))

    # break relevant classes into labs, lectures, and recitations
    class_types = {get_class_type(a) for a in relevant_classes}

    classes_by_type = {}
    for c in class_types:
        classes_by_type[c] = []

    for c in relevant_classes:
        class_type = get_class_type(c) # ex: class_type = "CS 120 Lecture" 
        classes_by_type[class_type].append(c)


    # generate list of each component that needs to be taken
    for a in product(*classes_by_type.values()):
        if valid_combo(a):
            yield a

def generate_schedules(data_file, target_classes):
    course = namedtuple('course', ['subject', 'course_num', 'instr_type', 'instr_method', 
                                   'sec', 'crn', 'title', 'day_time', 'instructor'])

    all_courses = []
    with open(data_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if "&" in row[2]:
                all_courses.append(course(row[0], row[1], "Lecture", row[3], row[4],
                                          row[5], row[6], row[7], row[8])) 
                all_courses.append(course(row[0], row[1], "Lab", row[3], row[4],
                                          row[5], row[6], row[7], row[8])) 
            else:
                all_courses.append(course(row[0], row[1], row[2], row[3], row[4],
                                          row[5], row[6], row[7], row[8])) 

#    for i in islice(get_valid_schedules(target_classes, all_courses), 1):
    for i in get_valid_schedules(target_classes, all_courses):
        yield i

#        print("------new combo------")
#        for n in i:
#            print(" ".join(n.day_time.split()[:5]), "      ",  n.subject, n.course_num, n.instr_method, "    ", n.crn)

def report(data_file, target_classes, title):
    for i in generate_schedules(data_file, target_classes):
        print(title, target_classes)
        for course in i:
            time_string = " ".join(course.day_time.split()[:5])
            print(",".join((time_string, course.subject, course.course_num
                                      , course.instr_method, course.crn )))

if __name__ == "__main__":
    target_classes = ["CS 171", "PSY 330", "COM 230", "PHIL 105", "STAT 201", "MATH 123"] #spring3
    report("fullSpring.csv", target_classes, "spring 3rd year")

#    target_classes = ["CS 172", "COM 310", "STAT 202", "INFO 330", "ECON 201"] # summer3
#    report("fullSummer.csv", target_classes, "summer 3rd year")

#    target_classes = ["SE 210", "CS 164", "CS 265", "CI 101", "ECON 202", "CS 270"] #fall4
#    report("fullFall.csv", target_classes, "fall 4th year")

#    target_classes = ["INFO 420", "SE 211", "CS 260", "CS 283", "INFO 210"] # winter4
#    report("fullWinter.csv", target_classes, "winter 4th year")

#    target_classes = ["CI 491", "SE 310", "SE 320",  "CS 350", "CS 380"] # fall5
#    report("fullFall.csv", target_classes, "fall 5th year")

#    target_classes = ["CI 492", "SE 311", "SE 410", "CS 303", "CS 385", "CS 360"] # winter5
#    report("fullWinter.csv", target_classes, "winter 5th year")

#    target_classes = ["CI 493", "INFO 310", "CS 281", "INFO 333", "CS 387"] # spring5
#    report("fullSpring.csv", target_classes, "spring 5th year")

