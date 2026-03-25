from django.db import models


class Enrollment(models.Model):
    student = models.IntegerField()
    course = models.IntegerField()

    status = models.CharField(max_length=50,default="enrolled")  # enrolled/completed
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)