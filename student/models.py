from django.contrib.auth.models import User
from django.db import models

from demoProject import settings

ATTENDANCE_STATUS = ((0, "A"), (1, "P"))
ASSIGNMENT_STATUS = ((0, "Incomplete"), (1, "Complete"))


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100)


class Student(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Attendance(models.Model):
    date = models.DateField()
    attendance = models.IntegerField(choices=ATTENDANCE_STATUS, default=0)
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

    class Meta:
        unique_together = ['student', 'date']


class Assignment(models.Model):
    title = models.DateField()
    date = models.DateField()
    progress = models.IntegerField(choices=ASSIGNMENT_STATUS, default=0)
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING);
