from django.db import models
from django.utils import timezone


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=100)
    a_description = models.TextField()
    assignment_points = models.IntegerField()
    assignment_file_path = models.CharField(max_length=100)
    course_id = models.IntegerField()
    due_date = models.DateTimeField(
        default=timezone.now)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)
    release_date = models.DateTimeField(
        default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.assignment_id)

# Create your models here.
