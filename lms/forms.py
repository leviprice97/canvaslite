from django import forms
from .models import Assignment
from .models import Course
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )


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






