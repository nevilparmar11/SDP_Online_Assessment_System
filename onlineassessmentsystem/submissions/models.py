from django.db import models

from problem.models import Problem
from users.models import User


def submissionFileName(instance, filename):
    fileNumber = Submission.objects.all.filter(user=instance.user, problem=instance.problem).count() + 1
    return 'submissions/' + instance.user.username.__str__() + "/" + instance.problem.problemId.__str__() + "/" + str(
        fileNumber) + "code.c "


class Submission(models.Model):
    submissionId = models.AutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    status = models.BooleanField()
    filePath = models.CharField(max_length=1000)
    submissionTime = models.DateTimeField(auto_now=True)


class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
