from django.db import models
from contest.models import Contest
from lab.models import Lab
from users.models import User


# Create your models here.

class Problem(models.Model):
    problemId = models.AutoField(primary_key=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, default="")
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, default="")
    title = models.CharField(null=False, max_length=50, default="DEFAULT-TITLE")
    description = models.CharField(null=False, max_length=1000, default="Default Problem description")

    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    DIFFICULTY = [(EASY, "EASY"), (MEDIUM, "MEDIUM"), (HARD, "HARD")]

    difficulty = models.CharField(choices=DIFFICULTY, max_length=6)
    points = models.IntegerField()
    durationTime = models.IntegerField()
    doesBelongToContest = models.BooleanField(default=False)


class ProblemComment(models.Model):
    pcId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    comment = models.CharField(max_length=2000)


class TestCase(models.Model):
    testCaseId = models.AutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    inputFile = models.FileField(upload_to=None, max_length=254)
    outputFile = models.FileField(upload_to=None, max_length=254)
