from django.db import models
from django.utils import timezone


class Course(models.Model):
    course_id = models.IntegerField(blank=False, null=False, unique=True)
    course_description = models.TextField()
    course_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.course_id)


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=100)
    a_description = models.TextField()
    assignment_points = models.IntegerField()
    assignment_file_path = models.CharField(max_length=100)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField(
        default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    release_date = models.DateTimeField(
        default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.assignment_name)


class Announcement(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
    announcement_name = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.announcement_name)


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.document.delete()
        super().delete(*args, **kwargs)
