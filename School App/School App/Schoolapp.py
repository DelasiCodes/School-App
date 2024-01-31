import pandas as pd

# Read the Excel sheet into a DataFrame
df = pd.read_excel('C:/Users/Student/Desktop/School App.xlsx')

# Prompt the user to enter the student ID
student_id = input("Enter the student ID: ")

# Find the row corresponding to the entered student ID
student_row = df.loc[df['Student ID'] == student_id]

# Check if the student ID exists in the DataFrame
if not student_row.empty:
    # Retrieve the student's name, class, and subjects
    student_name = student_row.iloc[0]['Name']
    student_class = student_row.iloc[0]['Class']
    subject_columns = ['Subject 1','Subject 2','Subject 3','Subject 4','Subject 5','Subject 6','Subject 7','Subject 8']
    student_subjects = []

    for column in subject_columns:
        if column in student_row.columns:
            subject_value = student_row[column].iloc[0]
            if pd.notna(subject_value):
                student_subjects.append(subject_value)

    # Display the student's information
    print("Student ID:", student_id)
    print("Name:", student_name)
    print("Class:", student_class)
    print("Subjects:", student_subjects)
else:
    print("Student ID not found.")