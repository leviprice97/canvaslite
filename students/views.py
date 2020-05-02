from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from courses.models import Course
from courses.models import Assignment
from courses.models import Grade
from courses.views import get_grade
from courses.models import User
from courses.views import StudentAssignmentGrade
from django.shortcuts import redirect

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super(StudentRegistrationView,
                       self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView,
                     self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView,
                        self).get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context


class StudentAssignmentList(ListView):
    model = Assignment
    fields = ['title', 'description', 'points', 'file', 'due_date']
    template_name = 'students/course/assignment_list.html'

    def get_queryset(self):
        qs = super(StudentAssignmentList, self).get_queryset()
        return qs.filter(course_id=Course.objects.get(id=self.kwargs['pk']))

    def get_context_data(self, **kwargs):
        context = super(StudentAssignmentList,
                        self).get_context_data(**kwargs)
        # get course object
        context['course'] = Course.objects.get(id=self.kwargs['pk'])

        return context

class StudentGradeBook(TemplateView):
    template_name = 'students/course/gradebook.html'
    course = None

    def get_student_grades(self, context):
        output = context
        student = User.objects.get(id=self.request.user.id)
        StudentGradeList = []
        earned_points = 0
        total_points = 0
        for assignment in self.course.assignments.all():
            try:
                StudentGradeList.append([Grade.objects.get(student = student, assignment = assignment),
                                         get_grade(Grade.objects.get(student = student, assignment = assignment).grade, Grade.objects.get(student=student, assignment=assignment).assignment.points)])

                earned_points += Grade.objects.get(student = student, assignment = assignment).grade
                total_points += Grade.objects.get(student=student, assignment=assignment).assignment.points
            except:
                StudentGradeList.append("-")
        output['course_grade'] = (get_grade(earned_points, total_points))
        output['grades']=(StudentGradeList)

        return output

    def get_context_data(self, **kwargs):
        context = super(StudentGradeBook,
                        self).get_context_data(**kwargs)
        self.course = Course.objects.get(id=self.kwargs['pk'])
        context['course'] = self.course
        context = self.get_student_grades(context)
        return context

class StudentAssignmentSubmit(StudentAssignmentGrade, CreateView):
    fields = ['submission_file']
    model = Grade

    def get(self, request, *args, **kwargs):
        try:
            Grade.objects.get(student=User.objects.get(id=self.request.user.id), assignment = Assignment.objects.get(id=self.kwargs['assignment_id']))
            return redirect('student_assignment_update', self.kwargs['pk'], self.kwargs['assignment_id'], self.request.user.id)
        except:
            return super(StudentAssignmentSubmit, self).get(request, *args, **kwargs)

    def post(self,  request, *args, **kwargs):
        StudentAssignmentGrade.success_url = reverse_lazy('student_course_assignment_list', kwargs={'pk': kwargs['pk']})
        return super(StudentAssignmentGrade, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.assignment = Assignment.objects.get(id=self.kwargs['assignment_id'])
        self.object.student = User.objects.get(id=self.request.user.id)
        self.object.save()
        return super().form_valid(form)

class StudentAssignmentUpdate(StudentAssignmentGrade, UpdateView):
    fields = ['submission_file']
    def get_object(self):
        return Grade.objects.get(student=self.kwargs['student_id'], assignment=self.kwargs['assignment_id'])

    def post(self,  request, *args, **kwargs):
        StudentAssignmentGrade.success_url = reverse_lazy('student_course_assignment_list', kwargs={'pk': kwargs['pk']})
        return super(StudentAssignmentGrade, self).post(request, *args, **kwargs)
