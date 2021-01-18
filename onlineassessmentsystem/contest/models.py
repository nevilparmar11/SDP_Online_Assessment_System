from enum import Enum
from django.db import models
from classroom.models import Classroom


# Create your models here.

class Contest(models.Model):
    contestId = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(null=False, max_length=50, default="DEFAULT-CONTEST")
    description = models.CharField(null=False, max_length=1000, default="Default Contest description")
    startTime = models.DateField()
    endTime = models.DateField()
    isPrivate = models.BooleanField(default=True)
    registeredUsersCount = models.IntegerField(default=0)

    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    DIFFICULTY = [(EASY, "EASY"), (MEDIUM, "MEDIUM"), (HARD, "HARD")]

    difficulty = models.CharField(choices=DIFFICULTY, max_length=6)
