import uuid
from datetime import datetime

from django.shortcuts import render, redirect
from .models import Classroom

'''
    Function to get all Classroom list details
'''


def list(request):
    classrooms = Classroom.objects.all()
    return render(request, './classroom/list.html', {'classrooms': classrooms})


'''
    Function to create Classroom
'''


def create(request):
    if request.method == "GET":
        return render(request, "classroom/create.html")

    userId = request.user
    name = request.POST['name']
    description = request.POST['description']
    semester = request.POST['semester']
    year = int(datetime.now().strftime('%Y'))
    classroomCode = uuid.uuid4()
    branch = request.POST['branch']
    newClassroom = Classroom(userId=userId, name=name, description=description,
                             semester=semester, year=year,
                             classroomCode=classroomCode, branch=branch)
    newClassroom.save()
    return redirect('/classroom/')


'''
    Function to get Classroom details
'''


def view(request):
    classId = request.GET['id']
    classroom = Classroom.objects.get(classId=classId)
    return render(request, './classroom/view.html', {'classroom': classroom})


'''
    Function to edit the Classroom details
'''


def edit(request):
    if request.method == "GET":
        classId = request.GET['id']
        classroom = Classroom.objects.get(classId=classId)
        return render(request, "classroom/edit.html", {'classroom': classroom})

    classId = request.POST['classId']
    classroom = Classroom.objects.get(classId=classId)

    classroom.name = request.POST['name']
    classroom.description = request.POST['description']
    classroom.semester = request.POST['semester']
    classroom.branch = request.POST['branch']
    classroom.save()
    return redirect('/classroom/')


'''
    Function to delete particular Classroom
'''


def delete(request):
    if request.method == "GET":
        classId = request.GET['id']
        classroom = Classroom.objects.get(classId=classId)
        return render(request, "classroom/delete.html", {'classroom': classroom})

    classId = request.POST['classId']
    classroom = Classroom.objects.get(classId=classId).delete()
    return redirect('/classroom/')
