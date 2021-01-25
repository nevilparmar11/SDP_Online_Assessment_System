from django.db import models
from contest.models import Contest
from lab.models import Lab
from users.models import User
from django.conf.urls.static import static
from django.conf import settings


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


# helper method # used
def testCaseFileName(instance, filename):
    totalTestCases = TestCase.objects.all().filter(problem=instance.problem).count() + 1
    mediaUrl = settings.MEDIA_URL + "problems/"
    return mediaUrl.join(['problems', instance.problem.problemId.__str__(), totalTestCases, filename])


class TestCase(models.Model):
    testCaseId = models.AutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    inputFile = models.FileField(upload_to=testCaseFileName, max_length=254)
    outputFile = models.FileField(upload_to=testCaseFileName, max_length=254)
