import json
import os

STUDENTS_FILE="students_details.json"


def load_students():
    if not os.path.exists(STUDENTS_FILE):
        return []
    with open(STUDENTS_FILE, "r") as f:
        return json.load(f)  




#save student  to json file
def save_students(students):
    with open(STUDENTS_FILE, "w") as f:
        json.dump( students, f, indent=4)
        #logging.info("saved the data succesfully")