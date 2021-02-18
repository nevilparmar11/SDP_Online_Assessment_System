import uuid
from datetime import datetime

from django.shortcuts import render, redirect
from .models import Classroom, ClassroomStudents
from users.decorators import faculty_required, student_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError


'''
    Function to get all Classroom list details
'''


@login_required(login_url='/users/login')
def list(request):

    user = request.user

    # classroom list will be shown according to th user type
    if user.isStudent:
        classroomStudents = ClassroomStudents.objects.filter(student=user)
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


@login_required(login_url='/users/login')
def view(request):

    user = request.user

    # if requested classroom not exists then
    try:
        classId = request.GET['id']
        classroom = Classroom.objects.get(classId=classId)
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return render(request, '404.html', {})

    if user.isStudent:

        # if student has joined classroom then only it is to be viewed
        try:
            classroomStudent = ClassroomStudents.objects.get(student=user, classroom=classroom)
            return render(request, './classroom/view.html', {'classroom': classroom})
        except ObjectDoesNotExist:
            return render(request, "accessDenied.html", {})
    else:

        # if faculty has created classroom then only it is to be viewed
        if classroom.user == user:
            return render(request, './classroom/view.html', {'classroom': classroom})
        else:
            return render(request, "accessDenied.html", {})


'''
    Function to edit the Classroom details
'''


@faculty_required()
def edit(request):

    if request.method == "GET":

        # if classroom not exists
        try:
            classId = request.GET['id']
            classroom = Classroom.objects.get(classId=classId)
            # if classroom is not belonging to logged faculty user then
            if classroom.user != request.user:
                return render(request, 'accessDenied.html', {})

        except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
            return render(request, '404.html', {})

        return render(request, "classroom/edit.html", {'classroom': classroom})

    try:
        classId = request.POST['classId']
        classroom = Classroom.objects.get(classId=classId)
        if classroom.user != request.user:
            return render(request, 'accessDenied.html', {})
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
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

        # if classroom not exists then
        try:
            classId = request.GET['id']
            classroom = Classroom.objects.get(classId=classId)
            # if classroom is not belonging to logged faculty user then
            if classroom.user != request.user:
                return render(request, 'accessDenied.html', {})
        except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
            return render(request, '404.html', {})

        return render(request, "classroom/delete.html", {'classroom': classroom})

    try:
        classId = request.POST['classId']
        classroom = Classroom.objects.get(classId=classId)
        if classroom.user != request.user:
            return render(request, 'accessDenied.html', {})
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
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
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return render(request, '404.html', {})

    # if Student had already joined the same class then
    try:
        classroomStudent = ClassroomStudents.objects.get(classroom=classroom, student=user)
        return render(request, "classroom/joinClassroom.html",
                      {"errorMessage": "You Have already Joined the Classroom"})
    except ObjectDoesNotExist:
        newClassroomStudent = ClassroomStudents(classroom=classroom, student=user)
        newClassroomStudent.save()
        return redirect('/classroom/')


'''
    Function to leave classroom by Student 
'''


@student_required()
def leaveClassroom(request):
    user = request.user
    if request.method == "GET":

        # if requested classroom not exists then
        try:
            classId = request.GET['id']
            classroom = Classroom.objects.get(classId=classId)
        except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
            return render(request, '404.html', {})

        # if student has joined classroom then only it is to be viewed
        try:
            classroomStudent = ClassroomStudents.objects.get(student=user, classroom=classroom)
            return render(request, './classroom/leaveClassroom.html', {'classroom': classroom})
        except ObjectDoesNotExist:
            return render(request, "accessDenied.html", {})

    # if student haven't joined classroom or classroom not exists
    try:
        user = request.user
        classroomCode = request.POST["classroomCode"]
        classroom = Classroom.objects.get(classroomCode=classroomCode)
        classroomStudent = ClassroomStudents.objects.get(classroom=classroom, student=user)
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return render(request, '404.html', {})

    classroomStudent.delete()
    return redirect('/classroom/')
