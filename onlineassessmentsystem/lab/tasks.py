from django.core.exceptions import ObjectDoesNotExist

from classroom.models import ClassroomStudents
from problem.models import Problem
from submissions.models import Submission
from .models import Lab, LabGrade

'''Function to find grade based on score'''


def findGrade(score):
    grade = 'F'
    if 85 <= score <= 100:
        grade = 'AA'
    elif 75 <= score < 85:
        grade = 'AB'
    elif 65 <= score < 75:
        grade = 'BB'
    elif 55 <= score < 65:
        grade = 'BC'
    elif 45 <= score < 55:
        grade = 'CC'
    elif 40 <= score < 45:
        grade = 'CD'
    elif score < 40:
        grade = 'FF'
    return grade


'''Function to perform Lab grading when Deadline is reached'''


def performLabGrading(labId):
    labId = int(labId)
    lab = Lab.objects.get(labId=labId)
    print("Lab Grading starts for the lab :- " + lab.title)
    problems = Problem.objects.filter(lab=lab)
    classroomStudents = ClassroomStudents.objects.filter(classroom=lab.classroom)
    for classroomStudent in classroomStudents:
        print("Performing Lab grading of :- " + classroomStudent.student.username)
        score = 0
        totalScore = 0

        for problem in problems:
            totalScore += problem.points
            submissions = Submission.objects.filter(problem=problem, user=classroomStudent.student)
            max_score = 0
            for submission in submissions:
                if submission.score > max_score:
                    max_score = submission.score
            score += max_score

        pct = int(score / totalScore * 100)
        grade = findGrade(pct)

        print(classroomStudent.student.username + " obtained " + str(score) + " out of " + str(totalScore))
        print("Grade :- " + grade)

        try:
            labGrade = LabGrade.objects.get(student=classroomStudent.student)
            labGrade.grade = grade
        except ObjectDoesNotExist:
            labGrade = LabGrade(student=classroomStudent.student, lab=lab, grade=grade)
        labGrade.save()

        print("Student :- "+classroomStudent.student.username+" Graded Successfully")
    print("Lab Grading Done for lab :- " + lab.title)
