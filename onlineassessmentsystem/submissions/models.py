from django.db import models
from problem.models import Problem
from users.models import User
# Create your models here.


class Submission(models.Model):
    submissionId = models.AutoField(primary_key=True)
    problemId = models.ForeignKey(Problem, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE) # TODO : update to user id
    score = models.IntegerField()
    status = models.BooleanField()
    filePath = models.FileField(upload_to="submissions/", max_length=256) # TODO
    submissionTime = models.DateTimeField(auto_now=True)


class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    submissionId = models.ForeignKey(Submission, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)