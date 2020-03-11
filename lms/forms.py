from django import forms
from .models import Assignment
from .models import Course


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = (
            'assignment_name', 'a_description', 'due_date', 'created_date',
            'release_date', 'assignment_points', 'course_id')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'course_name', 'course_description', 'course_id')
