import uuid
from django.db import models
from users.models import User


# Create your models here.

class Classroom(models.Model):
    classId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50, default="DEFAULT-CLASS")
    description = models.CharField(null=False, max_length=1000, default="Default description")
    semester = models.IntegerField(default=-1)
    year = models.IntegerField(default=-1)
    classroomCode = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    branch = models.CharField(max_length=50, default="Default branch")


# helper method used for saving input file to upload in specific folder with proper name
def classAttachmentFileName(instance, filename):
    totalClassAttachment = ClassComments.objects.all().filter(classroom=instance.classroom).count() + 1
    return 'classAttachments/' + instance.classroom.classId.__str__() + "/" + totalClassAttachment.__str__() + "_" + filename


class ClassComments(models.Model):
    ccId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    comment = models.CharField(max_length=2000)
    attachmentPath = models.FileField(upload_to=classAttachmentFileName, max_length=254, blank=True, null=True)


class ClassroomStudents(models.Model):
    classStudentId = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
