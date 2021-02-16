import datetime
import json
import os

import requests
from django.conf import settings
from django.http import JsonResponse

from problem.models import TestCase, Problem
from .models import Submission

'''Function to Compile code using API'''


def compileCode(code, stdIn):
    data = {
        'script': code,
        'language': 'c',
        'versionIndex': '4',
        'clientId': 'a92ce167568266c5f8f01df202603f6e',
        'clientSecret': '236048d32cb67fbf2dcb920f2673f6446fc2d26bec118453906130650ec70070',
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


'''Function to submit code'''


def submitCode(request):
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
    print(testCasesPassed / totalTestCases * problem.points)
    score = int(testCasesPassed / totalTestCases * problem.points)
    submission = Submission(problem_id=problemId, status=True, submissionTime=datetime.date.today(), user=request.user,
                            score=score,
                            filePath=filePath)
    submission.save()
    return JsonResponse({"passed": testCasesPassed, 'total': totalTestCases, 'score': score})
