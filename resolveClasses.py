#!/usr/bin/python3

class1 = ["CS", "161", "Lab", "Face To Face", "61", "42233", "Computer Programming II", "R 01:00 pm - 03:50 pm", "STAFF"]
class2 = ["CS", "161", "Lab", "Face To Face", "61", "42233", "Computer Programming II", "R 01:00 pm - 03:50 pm", "STAFF"]

def time_overlap(timeStringOne, timeStringTwo):
    daySetOne = set(timeStringOne.split()[0])
    daySetTwo = set(timeStringTwo.split()[0])

    days_overlap = daySetOne.intersection(daySetTwo):
       
    if not days_overlap:
        return False

    start1 = get_start_time(timeStringOne)
    end1 = get_end_time(timeStringOne)
    start2 = get_start_time(timeStringTwo)
    end2 = get_end_time(timeStringTwo)
    
    return class_time_overlap(start1, end1, start2, end2)

def get_start_time(time_string):
    combined_time =  int(time_string.split()[1].replace(":", ""))

    if time_string.split()[2] == "pm":
        military_time = combined_time + 1200
    
    return military_time 
    
def get_end_time(time_string):
    combined_time =  int(time_string.split()[-2].replace(":", ""))

    if time_string.split()[-1] == "pm":
        military_time = combined_time + 1200
    
    return military_time 

def class_time_overlap(start1, end1, start2, end2):
    if start1 < start2 and start2 < end1:
        return True
    elif start2 < start1 and start1 < end2:
        return True
    else:
        return False

print("They intersect" if time_overlap(class1[7], class2[7]) else "No intersection")
