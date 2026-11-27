import json
import os

Data_File = "planner_data.json"

#Load data from the JSON file
def load_data():
    if not os.path.exists(Data_File):
        return {}
    with open(Data_File, "r") as file:
        return json.load(file)


#Load data from the JSON file
def save_data(data):
    with open(Data_File, "w") as file:
        json.dump(data, file, indent=4)


def add_subject():
    #Load existing data
    data = load_data()

    #Get subject name
    subject_name = input("Enter the subject name: ").strip()
    if not subject_name:
        print("Subject name cannot be empty.")
        return

    try:
        #Get study hours
        study_hours = float(input("Enter study hours: "))
        if study_hours < 0:
            print("Study hours cannot be zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    #Store subject details
    subject = {
        "subject_name": subject_name,
        "study_hours": study_hours
    }

    #Add and save subject
    data["subjects"].append(subject)
    save_data(data)

    print(f"{subject_name} added successfully!")


def view_subjects():
    #Load saved subjects
    data = load_data()

    if not data["subjects"]:
        print("No subjects found.")
        return

    print("\n===== Your Subjects =====")

    #Display subjects with their study hours
    for index, subject in enumerate(data["subjects"], start=1):
        print(
            f"{index}. {subject['subject_name']} "
            f"- {subject['study_hours']} hours"
            )