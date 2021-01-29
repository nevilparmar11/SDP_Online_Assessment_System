from django.core.validators import FileExtensionValidator
from django.db import models
from contest.models import Contest
from lab.models import Lab
from users.models import User
from django.conf.urls.static import static
from django.conf import settings
import os
from django.core.exceptions import ValidationError

# Create your models here.

class Problem(models.Model):
    problemId = models.AutoField(primary_key=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, blank=True, null=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(null=False, max_length=50, default="DEFAULT-TITLE")
    description = models.CharField(null=False, max_length=1000, default="Default Problem description")

    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    DIFFICULTY = [(EASY, "EASY"), (MEDIUM, "MEDIUM"), (HARD, "HARD")]

    difficulty = models.CharField(choices=DIFFICULTY, max_length=6)
    points = models.IntegerField()
    timeLimit = models.IntegerField()
    doesBelongToContest = models.BooleanField()


class ProblemComment(models.Model):
    pcId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    comment = models.CharField(max_length=2000)


# helper method used for saving input file to upload in specific folder with proper name
def testCaseInputFileName(instance, filename):
    totalTestCases = TestCase.objects.all().filter(problem=instance.problem).count() + 1
    return 'problems/' + instance.problem.problemId.__str__() + "/" + totalTestCases .__str__()+"_input.txt"


# helper method used for saving output file to upload in specific folder with proper name
def testCaseOutputFileName(instance, filename):
    totalTestCases = TestCase.objects.all().filter(problem=instance.problem).count() + 1
    return 'problems/' + instance.problem.problemId.__str__() + "/" + totalTestCases .__str__()+"_output.txt"


# Helper Validator method
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


class TestCase(models.Model):
    testCaseId = models.AutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    inputFile = models.FileField(validators=[FileExtensionValidator(['txt'])], upload_to=testCaseInputFileName)
    outputFile = models.FileField(validators=[FileExtensionValidator(['txt'])], upload_to=testCaseOutputFileName)
