from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_q.models import Schedule

from classroom.models import Classroom
from users.models import User


# Create your models here.

class Lab(models.Model):
    labId = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=10, default="Default lab title")
    subject = models.CharField(null=False, max_length=50, default="DEFAULT-SUBJECT")
    description = models.CharField(null=False, max_length=1000, default="Default Lab description")
    deadline = models.DateTimeField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.labId)
        try:
            schedule = Schedule.objects.get(name=str(self.labId))
            schedule.next_run = self.deadline
            schedule.repeats = 1
            schedule.save()
            print("Schedule Updated for lab :- " + self.title)

        except ObjectDoesNotExist:
            Schedule.objects.create(
                name=str(self.labId),
                func="lab.tasks.performLabGrading",
                args=str(self.labId),
                schedule_type='O',
                repeats=1,
                next_run=self.deadline,
            )
            print("Schedule added for lab :- " + self.title)


class LabGrade(models.Model):
    labGradeId = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, null=False, default='F')
