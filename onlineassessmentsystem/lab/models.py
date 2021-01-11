from django.db import models
from classroom.models import Classroom

# Create your models here.

class Lab(models.Model):
    labId = models.AutoField(primary_key=True)
    classId = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subject = models.CharField(null=False, max_length=50, default="DEFAULT-SUBJECT")
    description = models.CharField(null=False, max_length=1000, default="Default Lab description")
    deadline = models.DateField()
