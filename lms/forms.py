from django import forms
from .models import Assignment
from .models import Course
from .models import Announcement
from .models import Document


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = (
            'assignment_name', 'a_description', 'due_date',
            'release_date', 'assignment_points', 'course_id')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'course_name', 'course_description', 'course_id')


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('course_id', 'announcement_name', 'description', 'created_date', 'updated_date')

        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
