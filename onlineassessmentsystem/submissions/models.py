from django.db import models
from problem.models import Problem
from users.models import User


class Submission(models.Model):
    submissionId = models.AutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    status = models.BooleanField()
    filePath = models.FileField(upload_to="submissions/", max_length=256)
    submissionTime = models.DateTimeField(auto_now=True)


class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
