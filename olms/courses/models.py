from django.db import models
from django.utils.timezone import now


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    level = models.CharField(max_length=50)
    instructor = models.IntegerField()
    category = models.IntegerField()
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.IntegerField()
    title = models.CharField(max_length=255)


    # removed auto_now_add
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    module = models.IntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()

    # (optional but good for consistency)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title