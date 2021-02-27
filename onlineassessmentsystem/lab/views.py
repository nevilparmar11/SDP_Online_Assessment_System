from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone

from classroom.models import Classroom, ClassroomStudents
from users.decorators import faculty_required
from .models import Lab

'''
    Function for Role based authorization of Classroom; upon provided the classId to the request parameter 
'''


def customRoleBasedClassroomAuthorization(request, classroom):
    user = request.user

    # If Faculty hasn't created classroom
    # or Student is not enrolled to the classroom
    if user.isStudent:
        try:
            classroomStudents = ClassroomStudents.objects.get(student=user, classroom=classroom)
        except ObjectDoesNotExist:
            return False
    else:
        if classroom.user != user:
            return False
    return True


'''
    Function for Role based authorization of lab; upon provided the labId to the request parameter 
'''


def customRoleBasedLabAuthorization(request, lab):
    user = request.user

    # If Faculty hasn't created the classroom for which current lab belongs
    # or If Student is not enrolled to the classroom for which current lab belongs
    if user.isStudent:
        try:
            classroomStudents = ClassroomStudents.objects.get(student=user, classroom=lab.classroom)
        except ObjectDoesNotExist:
            return False
    else:
        if lab.classroom.user != user:
            return False
    return True


'''
    Function to get lab based on provided Id
'''


def getLab(request):
    try:
        if request.method == "GET":
            labId = request.GET["id"]
        else:
            labId = request.POST["labId"]
        lab = Lab.objects.get(labId=labId)
        return True, labId, lab
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return False, None, None


'''
    Function to get lab based on provided Id
'''


def getClassroom(request):
    try:
        if request.method == "GET":
            classId = request.GET["classId"]
        else:
            classId = request.POST["classId"]
        classroom = Classroom.objects.get(classId=classId)
        return True, classId, classroom
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return False, None, None


'''
    Function which will convert Django DateTime to HTML DateTime
'''


def convertDjangoDateTimeToHTMLDateTime(lab):
    return lab.deadline.strftime('%Y-%m-%dT%H:%M')


'''
    Function to get all labs details list
'''


@login_required(login_url='/users/login')
def list(request):
    # If classroom not exist and If Classroom is not belonging to Faculty or Student
    result, classId, classroom = getClassroom(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedClassroomAuthorization(request, classroom):
        return render(request, 'accessDenied.html', {})

    # lab list will be shown belonging to the particular classroom
    labs = Lab.objects.filter(classroom=classroom)
    return render(request, 'lab/list.html', {'labs': labs, 'classId': classId, 'classroom': classroom, 'currentTime': timezone.now()})


'''
    Function to create lab
'''


@faculty_required()
def create(request):
    # GET request
    if request.method == "GET":
        # If classroom not exist and If Classroom is not belonging to Faculty or Student
        result, classId, classroom = getClassroom(request)
        if not result:
            return render(request, '404.html', {})
        if not customRoleBasedClassroomAuthorization(request, classroom):
            return render(request, 'accessDenied.html', {})
        print(str(timezone.now().strftime("%Y-%m-%dT%H:%M")))
        return render(request, 'lab/create.html', {'classId': classId, 'currentTime': str(timezone.now().strftime("%Y-%m-%dT%H:%M"))})

    # POST request
    # If Classroom not exist and If Classroom is not belonging to Faculty or Student
    result, classId, classroom = getClassroom(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedClassroomAuthorization(request, classroom):
        return render(request, 'accessDenied.html', {})

    # Saving the lab data
    title = request.POST['title']
    subject = request.POST['subject']
    description = request.POST['description']
    deadline = request.POST['deadline']
    newLab = Lab(title=title, subject=subject, description=description, deadline=deadline, classroom=classroom)
    newLab.save()
    return redirect('/labs?classId=' + classId)


'''
    Function to get lab details
'''


@login_required(login_url='/users/login')
def view(request):
    # If lab not exist and If Lab is not belonging to Faculty or Student
    result, labId, lab = getLab(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedLabAuthorization(request, lab):
        return render(request, 'accessDenied.html', {})
    return render(request, 'lab/view.html', {'lab': lab})


'''
    Function to edit the lab details
'''


@faculty_required()
def edit(request):
    # When request is GET
    if request.method == "GET":

        # If contest not exist and If Contest is not belonging to Faculty
        result, labId, lab = getLab(request)
        if not result:
            return render(request, '404.html', {})
        if not customRoleBasedLabAuthorization(request, lab):
            return render(request, 'accessDenied.html', {})

        lab_deadline = convertDjangoDateTimeToHTMLDateTime(lab)
        return render(request, 'lab/edit.html',
                      {'lab': lab, 'lab_deadline': lab_deadline, 'currentTime': str(timezone.now().strftime("%Y-%m-%dT%H:%M"))})

    # When request is POST
    # If contest not exist and If Contest is not belonging to Faculty
    result, labId, lab = getLab(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedLabAuthorization(request, lab):
        return render(request, 'accessDenied.html', {})

    # Updating Contest data
    lab.title = request.POST['title']
    lab.description = request.POST['description']
    lab.subject = request.POST['subject']
    lab.deadline = request.POST['deadline']
    lab.save()
    return redirect('/labs/?classId=' + str(lab.classroom.classId))


'''
    Function to delete particular lab
'''


@faculty_required()
def delete(request):
    # When request is GET then
    if request.method == "GET":

        # If contest not exist and If Contest is not belonging to Faculty
        result, labId, lab = getLab(request)
        if not result:
            return render(request, '404.html', {})
        if not customRoleBasedLabAuthorization(request, lab):
            return render(request, 'accessDenied.html', {})
        return render(request, 'lab/delete.html', {'lab': lab})

    # When request is POST
    # If contest not exist and If Contest is not belonging to Faculty
    result, labId, lab = getLab(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedLabAuthorization(request, lab):
        return render(request, 'accessDenied.html', {})
    lab.delete()
    return redirect('/labs/?classId=' + str(lab.classroom.classId))
