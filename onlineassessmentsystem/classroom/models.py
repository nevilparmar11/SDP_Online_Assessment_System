import uuid
from django.db import models
from users.models import User


# Create your models here.

class Classroom(models.Model):
    classId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # TODO: CHANGE IT TO FOREIGN KEY OF USER TABLE
    name = models.CharField(null=False, max_length=50, default="DEFAULT-CLASS")
    description = models.CharField(null=False, max_length=1000, default="Default description")
    semester = models.IntegerField(default=-1)
    year = models.IntegerField(default=-1)
    classroomCode = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)  # Randomly generated string
    branch = models.CharField(max_length=50, default="Default branch")


class ClassComments(models.Model):
    ccId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.DO_NOTHING)   # TODO: CHANGE IT TO FOREIGN KEY OF USER TABLE
    classId = models.ForeignKey(Classroom, on_delete=models.CASCADE)  # TODO: CHANGE IT TO FOREIGN KEY OF CLASS TABLE
    comment = models.CharField(max_length=2000)
    attachmentPath = models.FileField(upload_to="classAttachments/", max_length=254) # TODO: update
