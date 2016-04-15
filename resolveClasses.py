#!/usr/bin/python3

from itertools import product
from collections import namedtuple
import csv
from itertools import islice

def get_start_time(time_string):
    combined_time =  int(time_string.split()[1].replace(":", ""))

    military_time = combined_time
    if time_string.split()[2] == "pm":
        military_time = combined_time + 1200
    
    return military_time 
    
def get_end_time(time_string):
    combined_time =  int(time_string.split()[4].replace(":", ""))

    military_time = combined_time
    if time_string.split()[5] == "pm":
        military_time = combined_time + 1200
    
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

    

def get_class_type(class_info):
    return " ".join([class_info.name , class_info.instr_type])

def time_overlap(class1, class2):
    timeStringOne = class1.day_time
    timeStringTwo = class2.day_time

    daySetOne = set(timeStringOne.split()[0])
    daySetTwo = set(timeStringTwo.split()[0])

    no_day_overlap = not daySetOne.intersection(daySetTwo)
       
    if no_day_overlap:
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
    classes_compatible = lambda a,b:  a.crn == b.crn or not time_overlap(a,b)
    return all(classes_compatible(a,b) for a in classes for b in classes)

def get_valid_schedules(target_classes, class_schedule):
    # example input:
    # target_classes = ["ece 201", "se 210", engr 103"]
    # class_schedule = [["CS", "161", "Lab", "Face To Face", "61", "42233", "Computer Programming II", "R 01:00 pm - 03:50 pm", "STAFF"]
    #                  ,["CS", "161", "Lab", "Face To Face", "61", "42233", "Computer Programming II", "R 01:00 pm - 03:50 pm", "STAFF"]
    #                  ,["CS", "161", "Lab", "Face To Face", "61", "42233", "Computer Programming II", "R 01:00 pm - 03:50 pm", "STAFF"]] 

    # break class schedule to relevant classes
    relevant_classes = [a for a in class_schedule if a.name in target_classes ] 
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

def read_data(datafile):
    course = namedtuple('course', ['name', 'instr_type', 'instr_method', 'crn', 'day_time'])

    with open(datafile) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        data = [a for a in reader]

    for row in data:
        name = (row[0] + " " + row[1]).lower()
        instr_type = row[2].lower()
        instr_method = row[3].lower()
        crn = int(row[5])
        day_time = row[7]
        for a in instr_type.split("&"):
            yield course(name, a.strip(), instr_method, crn, day_time) 



def generate_schedules(data_file, target_classes):
    all_courses = read_data(data_file)

    for i in get_valid_schedules(target_classes, all_courses):
        yield i

def print_plan(title, classes):
    print("#" * 40)
    print(title, " ".join([a.name for a in classes]))
    print("#" * 40)

    for course in classes:
        time_string = " ".join(course.day_time.split()[:5])
        print(",".join((time_string, course.name, str(course.crn) )))
    print(" ")

def report(data_file, target_classes, title):
    [print_plan(title, i) for  i in generate_schedules(data_file, target_classes)]

if __name__ == "__main__":
    target_classes = ["cs 171", "psy 330", "com 230", "phil 105", "stat 201", "math 123"] #spring3
    report("fullSpring.csv", target_classes, "spring 3rd year")

#    target_classes = ["cs 172", "com 310", "stat 202", "info 330", "econ 201"] # summer3
#    report("fullSummer.csv", target_classes, "summer 3rd year")

#    target_classes = ["se 210", "cs 164", "cs 265", "ci 101", "econ 202", "cs 270"] #fall4
#    report("fullFall.csv", target_classes, "fall 4th year")

#    target_classes = ["info 420", "se 211", "cs 260", "cs 283", "info 210"] # winter4
#    report("fullWinter.csv", target_classes, "winter 4th year")

#    target_classes = ["ci 491", "se 310", "se 320",  "cs 350", "cs 380"] # fall5
#    report("fullFall.csv", target_classes, "fall 5th year")

#    target_classes = ["ci 492", "se 311", "se 410", "cs 303", "cs 385", "cs 360"] # winter5
#    report("fullWinter.csv", target_classes, "winter 5th year")

#    target_classes = ["ci 493", "info 310", "cs 281", "info 333", "cs 387"] # spring5
#    report("fullSpring.csv", target_classes, "spring 5th year")

