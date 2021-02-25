import os
import threading

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError

import submissions.views
from classroom.models import ClassroomStudents
from contest.models import Contest
from lab.models import Lab
from submissions.models import Submission
# from submissions.views import submitCode
from users.decorators import faculty_required
from .models import Problem, TestCase, ProblemComment

'''
    Function for Role based authorization of Problem; upon provided the pid to the request parameter 
'''


def customRoleBasedProblemAuthorization(request, problem, isItLab):
    user = request.user

    # If Faculty hasn't created classroom
    # or Student is not enrolled to the classroom
    if user.isStudent:
        try:
            if isItLab:
                classroomStudents = ClassroomStudents.objects.get(student=user, classroom=problem.lab.classroom)
            else:
                classroomStudents = ClassroomStudents.objects.get(student=user, classroom=problem.contest.classroom)
        except ObjectDoesNotExist:
            return False
    else:
        if ((isItLab and problem.lab.classroom.user != user) or (
                not isItLab and problem.contest.classroom.user != user)):
            return False

    return True


'''
    Function for Role based authorization of Problem of Test case; upon provided the pid to the request parameter 
'''


def customRoleBasedTestProblemAuthorization(request, problem):
    user = request.user

    if ((not problem.doesBelongToContest and problem.lab.classroom.user != user) or (
            problem.doesBelongToContest and problem.contest.classroom.user != user)):
        return False
    return True


'''
    Function for Role based authorization of Lab; upon provided the labId to the request parameter 
'''


def customRoleBasedLabAuthorization(request, lab):
    user = request.user

    # If Faculty hasn't created classroom
    # or Student is not enrolled to the classroom
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
    Function to get Problem based on provided pid
'''


def getProblem(request):
    try:

        # If request method is GET
        if request.method == "GET":
            pid = request.GET["pid"]
        else:
            pid = request.POST["pid"]
        problem = Problem.objects.get(problemId=pid)
        return True, pid, problem
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return False, None, None


'''
    Function to get Test Case based on provided tid
'''


def getTestCase(request):
    try:

        # If request method is GET
        if request.method == "GET":
            return False, None, None
        else:
            tid = request.POST["tid"]
        print(tid)
        testCase = TestCase.objects.get(testCaseId=tid)
        return True, tid, testCase
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return False, None, None


'''
    Function to get Contest/Lab based on provided Id
'''


def getContestOrLab(request):
    try:
        isItLab = False
        labId = None
        contestId = None

        if request.method == "GET":
            if (request.GET.get('labId')):
                labId = request.GET["labId"]
            else:
                contestId = request.GET["contestId"]
        else:
            if (request.POST.get('contestId')):
                contestId = request.POST["contestId"]
            else:
                labId = request.POST["labId"]

        if (not labId and contestId):
            contest = Contest.objects.get(contestId=contestId)
            isItLab = False
            return True, contestId, contest, isItLab
        elif (not contestId and labId):
            lab = Lab.objects.get(labId=labId)
            isItLab = True
            return True, labId, lab, isItLab
        else:
            return False, None, None, False

    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        print('exception')
        return False, None, None, False


'''
    Function which will convert Django DateTime to HTML DateTime
'''


def convertDjangoDateTimeToHTMLDateTime(contest):
    # Converting Datetime field into HTML formatted string
    startTimeString = str(contest.startTime.strftime("%Y-%m-%dT%H:%M"))
    endTimeString = str(contest.endTime.strftime("%Y-%m-%dT%H:%M"))
    return startTimeString, endTimeString


'''
    Function to get list of all Test Cases belonging to the Problem
'''


@faculty_required()
def testList(request):
    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedTestProblemAuthorization(request, problem):
        return render(request, 'accessDenied.html', {})

    testCases = TestCase.objects.filter(problem=problem)
    isOver = False
    if problem.doesBelongToContest:
        if timezone.now() >= problem.contest.endTime:
            isOver = True
    else:
        if timezone.now() >= problem.lab.deadline:
            isOver = True
    return render(request, 'problem/testsList.html',
                  {'tests': testCases, 'pid': pid, 'problem': problem, 'isOver': isOver})


'''Function which executes thread in background'''


def reevaluateSubmissionThread(problemId, request):
    problem = Problem.objects.get(problemId=problemId)
    print("Submission Reevaluation Started for problem :- ", problem.title)
    submittedSubmissions = Submission.objects.filter(problem=problem)
    for submission in submittedSubmissions:
        uploadDirectory = settings.MEDIA_ROOT
        file = open(os.path.join(uploadDirectory, submission.filePath), "r")
        code = file.read()
        request.GET._mutable = True
        request.GET["code"] = code
        request.GET["problemId"] = problemId
        submissions.views.submitCode(request, update=True, submission=submission)
        file.close()
    print("Submission Reevaluation Finished for problem :- ", problem.title)


'''Function for reevaluating submissions after updating test cases'''


def reEvaluateSubmissions(request, problemId):
    thread = threading.Thread(target=reevaluateSubmissionThread, args=[problemId, request])
    thread.setDaemon(True)
    thread.start()


'''
    Function to create Test Case belonging to the Problem
'''


@faculty_required()
def testCreate(request):
    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedTestProblemAuthorization(request, problem):
        return render(request, 'accessDenied.html', {})

    try:
        outputFile = request.FILES['outputFile']
        inputFile = request.FILES['inputFile']
    except MultiValueDictKeyError:
        return render(request, 'problem/testsList.html', {"errorMessage": "Files are not selected"})

    newTestcase = TestCase(problem=problem, inputFile=inputFile, outputFile=outputFile)
    newTestcase.save()
    reEvaluateSubmissions(request, problem.problemId)
    return redirect('/problems/tests?pid=' + pid)


'''
    Function to create Test Case belonging to the Problem
'''


@faculty_required()
def testDelete(request):
    result, tid, testCase = getTestCase(request)
    if not result:
        return render(request, '404.html', {})
    else:
        if not customRoleBasedTestProblemAuthorization(request, testCase.problem):
            return render(request, 'accessDenied.html', {})

    testCase.inputFile.delete()
    testCase.outputFile.delete()
    testCase.delete()
    reEvaluateSubmissions(request, testCase.problem.problemId)
    return redirect('/problems/tests/?pid=' + str(testCase.problem.problemId))


'''
    Function to get list of all Problems
'''


@login_required(login_url='/users/login')
def list(request):
    # If classroom not exist and If Classroom is not belonging to Faculty or Student
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    idName = ""
    # Problem list will be shown belonging to the particular contest or lab
    isOver = False
    isStarted = False
    hours = timezone.now().hour
    minutes = timezone.now().minute
    seconds = timezone.now().second

    if isItLab:
        idName = "labId"
        problems = Problem.objects.filter(lab=object, doesBelongToContest=False)
        if timezone.now() >= object.deadline:
            isOver = True
    else:
        idName = "contestId"
        problems = Problem.objects.filter(contest=object, doesBelongToContest=True)
        if timezone.now() >= object.endTime:
            isOver = True
        hours = object.endTime.hour - timezone.now().hour
        minutes = object.endTime.minute - timezone.now().minute
        seconds = object.endTime.second - timezone.now().second
        if timezone.now() >= object.startTime and timezone.now() <= object.endTime:
            isStarted = True;

    return render(request, 'problem/list.html',
                  {'problems': problems, 'idName': idName, 'idValue': objectId, 'isItLab': isItLab, "object": object, 'isOver': isOver, 'isStarted': isStarted, 'hours': hours, 'minutes': minutes, 'seconds': seconds})


'''
    Function to create Problem
'''


@faculty_required()
def create(request):
    # If classroom not exist and If Classroom is not belonging to Faculty or Student
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    idName = ""
    if isItLab:
        idName = "labId"
    else:
        idName = "contestId"

    if request.method == 'GET':
        return render(request, 'problem/create.html', {'idName': idName, 'idValue': objectId})

    # Saving the Problem data
    title = request.POST['title']
    description = request.POST['description']
    difficulty = request.POST['difficulty']
    points = request.POST['points']
    timeLimit = request.POST['timeLimit']

    if isItLab:
        newProblem = Problem(title=title, description=description, difficulty=difficulty, points=points,
                             timeLimit=timeLimit, doesBelongToContest=False, lab=object)
    else:
        newProblem = Problem(title=title, description=description, difficulty=difficulty, points=points,
                             timeLimit=timeLimit, doesBelongToContest=True, contest=object)

    newProblem.save()
    return redirect("/problems/?" + idName + "=" + objectId)


'''
    Function to get Problem details
'''


@login_required(login_url='/users/login')
def view(request):
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedProblemAuthorization(request, problem, isItLab):
        return render(request, 'accessDenied.html', {})

    idName = ""
    isOver = False
    if isItLab:
        idName = "labId"
        if timezone.now() >= object.deadline:
            isOver = True
    else:
        idName = "contestId"
        if timezone.now() >= object.endTime:
            isOver = True
    return render(request, 'problem/view.html',
                  {'problem': problem, 'idName': idName, 'idValue': objectId, 'isOver': isOver})


'''
    Function to edit the Problem details
'''


@faculty_required()
def edit(request):
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedProblemAuthorization(request, problem, isItLab):
        return render(request, 'accessDenied.html', {})

    idName = ""
    if isItLab:
        problem.doesBelongToContest = False
        idName = "labId"
    else:
        problem.doesBelongToContest = True
        idName = "contestId"

    if request.method == 'GET':
        return render(request, 'problem/edit.html', {'problem': problem, 'idName': idName, 'idValue': objectId})

    # Saving the Problem data
    problem.title = request.POST['title']
    problem.description = request.POST['description']
    problem.difficulty = request.POST['difficulty']
    problem.points = request.POST['points']
    problem.timeLimit = request.POST['timeLimit']
    problem.save()
    return redirect('/problems/view?pid=' + str(problem.problemId) + "&&" + idName + "=" + objectId)


'''
    Function to delete particular Problem
'''


@faculty_required()
def delete(request):
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedProblemAuthorization(request, problem, isItLab):
        return render(request, 'accessDenied.html', {})

    idName = ""
    if isItLab:
        problem.doesBelongToContest = False
        idName = "labId"
    else:
        problem.doesBelongToContest = True
        idName = "contestId"

    if request.method == 'GET':
        return render(request, 'problem/delete.html', {'problem': problem, 'idName': idName, 'idValue': objectId})

    problem.delete()
    return redirect('/problems?' + idName + "=" + objectId)


''' 
    function to list out the problem comments
'''


@login_required(login_url='/users/login')
def comments(request):
    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedProblemAuthorization(request, problem, not problem.doesBelongToContest):
        return render(request, 'accessDenied.html', {})

    problemComments = ProblemComment.objects.filter(problem=problem)
    objectName = ""
    objectId = 0
    if problem.doesBelongToContest:
        objectName = "contestId"
        objectId = problem.contest.contestId
    else:
        objectName = "labId"
        objectId = problem.lab.labId
    return render(request, 'problem/commentsList.html',
                  {'comments': problemComments, 'pid': pid, 'problem': problem, 'objectName': objectName,
                   'objectId': objectId})


'''
    function to create the problem comments
'''


@login_required(login_url='/users/login')
def commentCreate(request):
    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedProblemAuthorization(request, problem, not problem.doesBelongToContest):
        return render(request, 'accessDenied.html', {})

    comment = request.POST["comment"]
    user = request.user
    newComment = ProblemComment(comment=comment, user=user, problem=problem)
    newComment.save()

    return redirect('/problems/comments/?pid' + "=" + pid)


@faculty_required()
def testEdit(request):
    result, tid, testCase = getTestCase(request)
    if not result:
        return render(request, '404.html', {})
    else:
        if not customRoleBasedTestProblemAuthorization(request, testCase.problem):
            return render(request, 'accessDenied.html', {})
    input = request.POST.get("input")
    output = request.POST.get("output")
    input = input.replace('\r', '')
    output = output.replace('\r', '')
    fpInput = open(os.path.join(settings.BASE_DIR, testCase.inputFile.url[1:]), "w")
    fpInput.write(input)
    fpInput.close()
    fpOutput = open(os.path.join(settings.BASE_DIR, testCase.outputFile.url[1:]), "w")
    fpOutput.write(output)
    fpOutput.close()
    reEvaluateSubmissions(request, testCase.problem.problemId)
    return redirect('/problems/tests/?pid=' + str(testCase.problem.problemId))
