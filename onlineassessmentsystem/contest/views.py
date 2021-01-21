from django.shortcuts import render, redirect
from .models import Contest
from classroom.models import ClassroomStudents, Classroom
from users.decorators import faculty_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
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
    Function for Role based authorization of Contest; upon provided the contestId to the request parameter 
'''


def customRoleBasedContestAuthorization(request, contest):
    user = request.user

    # If Faculty hasn't created the classroom for which current contest belongs
    # or If Student is not enrolled to the classroom for which current contest belongs
    if user.isStudent:
        try:
            classroomStudents = ClassroomStudents.objects.get(student=user, classroom=contest.classroom)
        except ObjectDoesNotExist:
            return False
    else:
        if contest.classroom.user != user:
            return False
    return True


'''
    Function to get Contest based on provided Id
'''


def getContest(request):

    try:
        if request.method == "GET":
            contestId = request.GET["id"]
        else:
            contestId = request.POST["contestId"]
        contest = Contest.objects.get(contestId=contestId)
        return True, contestId, contest
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return False, None, None


'''
    Function to get Contest based on provided Id
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


#def convertDjangoDateTimeToHTMLDateTime(contest):



'''
    Function to get all Classroom list details
'''


@login_required(login_url='/users/login')
def list(request):

    # If classroom not exist and If Classroom is not belonging to Faculty or Student
    result, classId, classroom = getClassroom(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedClassroomAuthorization(request, classroom):
        return render(request, 'accessDenied.html', {})

    # Contest list will be shown belonging to the particular classroom
    contests = Contest.objects.filter(classroom=classroom)
    return render(request, 'contest/list.html', {'contests': contests, 'classId': classId})


'''
    Function to create Classroom
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
        return render(request, 'contest/create.html', {'classId': classId})

    # POST request
    # If Classroom not exist and If Classroom is not belonging to Faculty or Student
    result, classId, classroom = getClassroom(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedClassroomAuthorization(request, classroom):
        return render(request, 'accessDenied.html', {})

    # Saving the Contest data
    title = request.POST['title']
    description = request.POST['description']
    startTime = request.POST['startTime']
    endTime = request.POST['endTime']
    startTimeDate = datetime.fromisoformat(startTime)
    endTimeDate = datetime.fromisoformat(endTime)
    print(startTimeDate, endTimeDate)

    # Remaining Implementation of isPrivate in create.html and views.py
    isPrivate = False
    difficulty = request.POST['difficulty']

    newContest = Contest(classroom=classroom, title=title, description=description,
                         startTime=startTimeDate, endTime=endTimeDate,
                         isPrivate=isPrivate, difficulty=difficulty)
    newContest.save()
    return redirect('/contests?classId=' + classId)


'''
    Function to get Classroom details
'''


@login_required(login_url='/users/login')
def view(request):

    # If contest not exist and If Contest is not belonging to Faculty or Student
    result, contestId, contest = getContest(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedContestAuthorization(request, contest):
        return render(request, 'accessDenied.html', {})
    return render(request, 'contest/view.html', {'contest': contest})


'''
    Function to edit the Classroom details
'''


@faculty_required()
def edit(request):

    # When request is GET
    if request.method == "GET":

        # If contest not exist and If Contest is not belonging to Faculty
        result, contestId, contest = getContest(request)
        if not result:
            return render(request, '404.html', {})
        if not customRoleBasedContestAuthorization(request, contest):
            return render(request, 'accessDenied.html', {})
 #       startTimeString, endTimeString = convertDjangoDateTimeToHTMLDateTime(contest)
        return render(request, 'contest/edit.html', {'contest': contest, 'startTime': startTimeString, 'endTime': endTimeString})

    # When request is POST
    # If contest not exist and If Contest is not belonging to Faculty
    result, contestId, contest = getContest(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedContestAuthorization(request, contest):
        return render(request, 'accessDenied.html', {})

    # Updating Contest data
    contest.title = request.POST['title']
    contest.description = request.POST['description']
    contest.startTime = request.POST['startTime']
    contest.endTime = request.POST['endTime']

    # Remaining Implementation of isPrivate in create.html and views.py
    contest.isPrivate = False
    contest.difficulty = request.POST['difficulty']
    contest.save()
    return redirect('/contests/?classId='+str(contest.classroom.classId))


'''
    Function to delete particular Classroom
'''


@faculty_required()
def delete(request):

    # When request is GET then
    if request.method == "GET":

        # If contest not exist and If Contest is not belonging to Faculty
        result, contestId, contest = getContest(request)
        if not result:
            return render(request, '404.html', {})
        if not customRoleBasedContestAuthorization(request, contest):
            return render(request, 'accessDenied.html', {})
        return render(request, 'contest/delete.html', {'contest': contest})

    # When request is POST
    # If contest not exist and If Contest is not belonging to Faculty
    result, contestId, contest = getContest(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedContestAuthorization(request, contest):
        return render(request, 'accessDenied.html', {})
    contest.delete()
    return redirect('/contests/?classId='+str(contest.classroom.classId))
