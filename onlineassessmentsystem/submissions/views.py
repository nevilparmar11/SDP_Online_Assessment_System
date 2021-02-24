import datetime
import json
import os
from urllib.parse import urlencode

import pytz
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from classroom.models import ClassroomStudents
from problem.models import TestCase, Problem
from users.models import User
from .models import Submission

utc = pytz.UTC

loginRedirectMessage = urlencode({'msg': 'Please Login'})

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


'''Function to Compile code using API'''


def compileCode(code, stdIn):
    data = {
        'script': code,
        'language': 'c',
        'versionIndex': '4',
        'clientId': settings.API_CLIENT_ID,
        'clientSecret': settings.API_CLIENT_SECRET,
        'stdin': stdIn
    }
    url = 'https://api.jdoodle.com/v1/execute'
    r = requests.post(url, data=json.dumps(data), headers={"content-type": "application/json"})
    r = r.json()
    if 'error' in r:
        return r['error']
    else:
        return r['output']


'''Function to generate file upload Path'''


def getSubmissionFilePath(request, user, problem):
    fileNumber = Submission.objects.filter(user=user, problem=problem).count() + 1
    return "submissions/" + user.username + "/" + str(problem.problemId) + "/code_" + str(fileNumber) + ".c"


'''Function to compare code's output with expected output of test case'''


def compareOutput(codeOutput, testcaseOutput):
    if len(codeOutput) != len(testcaseOutput):
        return False
    for i in range(len(codeOutput)):
        if codeOutput[i] != testcaseOutput[i]:
            return False
    return True


@login_required(login_url='/users/login?' + loginRedirectMessage)
def runCode(request):
    code = request.GET.get('code')
    stdin = request.GET.get('stdin')
    output = compileCode(code, stdin)
    return JsonResponse({"output": output})


'''Function to submit code'''


@login_required(login_url='/users/login?' + loginRedirectMessage)
def submitCode(request, update=False, submission=None):
    code = request.GET.get('code')
    problemId = request.GET.get('problemId')
    problem = Problem.objects.get(problemId=problemId)
    filePath = getSubmissionFilePath(request, request.user, problem)
    uploadDirectory = settings.MEDIA_ROOT

    try:
        file = open(os.path.join(uploadDirectory, filePath), 'w')
    except FileNotFoundError:
        os.makedirs(os.path.dirname(os.path.join(uploadDirectory, filePath)))
        file = open(os.path.join(uploadDirectory, filePath), 'w')

    file.write(code)
    file.close()
    testCases = TestCase.objects.filter(problem=problem)
    testCasesPassed = 0
    totalTestCases = len(testCases)

    for testCase in testCases:
        fpInput = open(os.path.join(settings.BASE_DIR, testCase.inputFile.url[1:]), "r")
        stdin = fpInput.read()
        fpInput.close()
        output = compileCode(code, stdin)
        fpOutput = open(os.path.join(settings.BASE_DIR, testCase.outputFile.url[1:]), "r")
        if compareOutput(output, fpOutput.read()):
            testCasesPassed += 1
        fpOutput.close()

    score = int(testCasesPassed / totalTestCases * problem.points)
    if update:
        submission.score = score
        submission.save()
        return
    submission = Submission(problem_id=problemId, status=True, submissionTime=datetime.date.today(), user=request.user,
                            score=score,
                            filePath=filePath)
    submission.save()
    return JsonResponse({"passed": testCasesPassed, 'total': totalTestCases, 'score': score})


'''Function To display List of submissions'''


@login_required(login_url='/users/login?' + loginRedirectMessage)
def list(request):
    problemId = request.GET.get('problemId')
    page = request.GET.get('page', 1)

    if problemId is None:
        return render(request, '404.html')

    try:
        problem = Problem.objects.get(problemId=problemId)
    except ObjectDoesNotExist:
        return render(request, '404.html')

    if not customRoleBasedProblemAuthorization(request, problem, not problem.doesBelongToContest):
        return render(request, 'accessDenied.html')
    username = request.GET.get("username")

    isOver = False
    user = request.user
    if problem.doesBelongToContest:
        if timezone.now() >= problem.contest.endTime:
            isOver = True
    else:
        if timezone.now() >= problem.lab.deadline:
            isOver = True

    if username is not None:
        try:
            user = User.objects.get(username=username)
            submissionsList = Submission.objects.filter(problem=problem, user=user)
        except ObjectDoesNotExist:
            submissionsList = []

    else:
        submissionsList = Submission.objects.filter(problem=problem)
    paginator = Paginator(submissionsList, 10)
    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        submissions = paginator.page(1)
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)

    return render(request, 'submissions/list.html',
                  {'problem': problem, 'submissions': submissions, "username": username, 'isOver': isOver,
                   'user': user})


@login_required(login_url='/users/login?' + loginRedirectMessage)
def view(request):
    submissionId = request.GET.get('submissionId')
    if submissionId is None:
        return render(request, '404.html')

    try:
        submission = Submission.objects.get(submissionId=submissionId)
    except ObjectDoesNotExist:
        return render(request, '404.html')

    if not customRoleBasedProblemAuthorization(request, submission.problem, not submission.problem.doesBelongToContest):
        return render(request, 'accessDenied.html')

    # Submission can be viewed by other participants only after contest is over
    if submission.problem.doesBelongToContest:
        if timezone.now() < submission.problem.contest.endTime and submission.user != request.user:
            return render(request, 'accessDenied.html')
    else:
        if timezone.now() < submission.problem.lab.deadline and submission.user != request.user:
            return render(request, 'accessDenied.html')

    uploadDirectory = settings.MEDIA_ROOT
    file = open(os.path.join(uploadDirectory, submission.filePath), "r")
    code = file.read()
    file.close()
    return render(request, 'submissions/view.html', {'submission': submission, 'code': code})
