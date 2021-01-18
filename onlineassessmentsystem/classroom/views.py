import uuid
from datetime import datetime

from django.shortcuts import render, redirect
from .models import Classroom, ClassroomStudents
from users.decorators import faculty_required, student_required
from django.core.exceptions import ObjectDoesNotExist

'''
    Function to get all Classroom list details
'''


def list(request):
    user = request.user
    if user.isStudent:
        classroomStudents = ClassroomStudents.objects.all().select_related('student')
        return render(request, './classroom/list.html', {'classroomStudents': classroomStudents})
    else:
        classrooms = Classroom.objects.filter(user=user)
        return render(request, './classroom/list.html', {'classrooms': classrooms})


'''
    Function to create Classroom
'''


@faculty_required()
def create(request):
    if request.method == "GET":
        return render(request, "classroom/create.html")

    user = request.user
    name = request.POST['name']
    description = request.POST['description']
    semester = request.POST['semester']
    year = int(datetime.now().strftime('%Y'))
    classroomCode = uuid.uuid4()
    branch = request.POST['branch']
    newClassroom = Classroom(user=user, name=name, description=description,
                             semester=semester, year=year,
                             classroomCode=classroomCode, branch=branch)
    newClassroom.save()
    return redirect('/classroom/')


'''
    Function to get Classroom details
'''


def view(request):
    try:
        classId = request.GET['id']
        classroom = Classroom.objects.get(classId=classId)
    except ObjectDoesNotExist:
        return render(request, '404.html', {})

    return render(request, './classroom/view.html', {'classroom': classroom})


'''
    Function to edit the Classroom details
'''


@faculty_required()
def edit(request):
    if request.method == "GET":
        try:
            classId = request.GET['id']
            classroom = Classroom.objects.get(classId=classId)
        except ObjectDoesNotExist:
            return render(request, '404.html', {})

        return render(request, "classroom/edit.html", {'classroom': classroom})

    try:
        classId = request.POST['classId']
        classroom = Classroom.objects.get(classId=classId)
    except ObjectDoesNotExist:
        return render(request, '404.html', {})

    classroom.name = request.POST['name']
    classroom.description = request.POST['description']
    classroom.semester = request.POST['semester']
    classroom.branch = request.POST['branch']
    classroom.save()
    return redirect('/classroom/')


'''
    Function to delete particular Classroom
'''


@faculty_required()
def delete(request):
    if request.method == "GET":
        try:
            classId = request.GET['id']
            classroom = Classroom.objects.get(classId=classId)
        except ObjectDoesNotExist:
            return render(request, '404.html', {})

        return render(request, "classroom/delete.html", {'classroom': classroom})

    try:
        classId = request.POST['classId']
        classroom = Classroom.objects.get(classId=classId)
    except ObjectDoesNotExist:
        return render(request, '404.html', {})

    classroom.delete()
    return redirect('/classroom/')


'''
    Function to join classroom by Student
'''


@student_required()
def joinClassroom(request):
    if request.method == "GET":
        return render(request, "classroom/joinClassroom.html", {})

    # if classroom code is not valid or classroom not exists then
    try:
        user = request.user
        classroomCode = request.POST["classroomCode"]
        classroom = Classroom.objects.get(classroomCode=classroomCode)
    except ObjectDoesNotExist:
        return render(request, '404.html', {})

    # if Student had already joined the same class then
    try:
        classroomStudent = ClassroomStudents.objects.get(classroom=classroom, student=user)
        return render(request, "classroom/joinClassroom.html", {"errorMessage": "You Have already Joined the Classroom"})
    except ObjectDoesNotExist:
        newClassroomStudent = ClassroomStudents(classroom=classroom, student=user)
        newClassroomStudent.save()
        return redirect('/classroom/')


'''
    Function to leave classroom by Student 
'''


@student_required()
def leaveClassroom(request):
    try:
        user = request.user
        classroomCode = request.POST["classroomCode"]
        classroom = Classroom.objects.get(classroomCode=classroomCode)
        classroomStudent = ClassroomStudents.objects.get(classroom=classroom, student=user)
    except ObjectDoesNotExist:
        return render(request, '404.html', {})

    classroomStudent.delete()
    return redirect('/classroom/')
