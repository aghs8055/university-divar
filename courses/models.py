from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    department = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    course_number = models.IntegerField(null=False)
    group_number = models.IntegerField(null=False)
    teacher_name = models.CharField(max_length=50, null=False, blank=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    DAYS = ((0, 'Saturday'), (1, 'Sunday'), (2, 'Monday'), (3, 'Tuesday'), (4, 'Thursday'))
    first_day = models.IntegerField(choices=DAYS, null=False)
    second_day = models.IntegerField(choices=DAYS, null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    image = models.ImageField(upload_to='upload/')
    user_type = models.CharField(max_length=1, choices=(('S', 'Student'), ('T', 'Teacher')), null=True)


