"""
Try-It Yourself Exercise: GRade Calculator

Given a dict of student names and their grades, compute letter grades
and group students by their letter grades.

"""


def letter_grade(score):
    """
    Convert a numeric score to a letter grade. (This functions has no bugs.)

    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def convert_grades(student_grades):
    """
    Convert student numeric grades to letter grades.
    Args:
    student_letter_grades:Dict of {student_name: letter_grade}

    Returns:
    Dict of {letter_grade: [list_of_students]}

    """
    letter_grades = {}
    for student, grade in student_grades.items():
        letter_grades[student] = letter_grade(grade)

    return letter_grades


def group(student_letter_grades):

    grade_groups = {}
    for student, grade in student_letter_grades.items():

        if grade not in grade_groups:
            grade_groups[grade] = []
        grade_groups[grade].append(student)

    return grade_groups


# Test the functions
students = {
    "Aisha": 95,
    "Carlos": 87,
    "Priya": 92,
    "Jamal": 78,
    "Fatima": 83,
    "Li Wei": 65,
    "Sam": 58,
    "Maya": 91,
}

# We want to get something like this { A: ['Aysha','Priya', 'Maya'], B:[.......]}

grades = convert_grades(students)
grouped = group(grades)

print("Students grouped by letter grade: ")
print(grouped)
