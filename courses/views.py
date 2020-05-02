from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from .forms import ModuleFormSet
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module, Content
from django.views.generic.detail import DetailView
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from .models import Subject
from students.forms import CourseEnrollForm
from .models import Assignment, Grade
from .models import User
from django.contrib.contenttypes.models import ContentType


class OwnerMixin(object):
	def get_queryset(self):
		qs = super(OwnerMixin, self).get_queryset()
		return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
	model = Course
	fields = ['subject', 'title', 'slug', 'overview']
	success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
	fields = ['subject', 'title', 'slug', 'overview']
	success_url = reverse_lazy('manage_course_list')
	template_name = "courses/manage/course/form.html"


class ManageCourseListView(OwnerCourseMixin, ListView):
	template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin,
					   OwnerCourseEditMixin,
					   CreateView):
	permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,
					   OwnerCourseEditMixin,
					   UpdateView):
	permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
					   OwnerCourseMixin,
					   DeleteView):
	template_name = 'courses/manage/course/delete.html'
	permission_required = 'courses.delete_course'


class OwnerAssignmentMixin(LoginRequiredMixin):
	model = Assignment
	fields = ['title', 'description', 'points', 'file', 'due_date']

	def post(self, request, *args, **kwargs):
		OwnerAssignmentMixin.success_url = reverse_lazy('course_assignment_list', kwargs={'pk': kwargs['pk']})

		return super(OwnerAssignmentMixin, self).post(request, *args, **kwargs)

	def form_valid(self, form):
		course = Course.objects.get(pk=self.kwargs['pk'])
		self.object = form.save(commit=False)
		self.object.course = course
		self.object.save()
		return super().form_valid(form)


class OwnerAssignmentEditMixin(OwnerAssignmentMixin, OwnerEditMixin):
	fields = ['title', 'description', 'points', 'file', 'due_date']

	template_name = 'courses/manage/assignment/create.html'


class AssignmentCreateView(OwnerAssignmentEditMixin, CreateView):
	fields = ['title', 'description', 'points', 'file', 'due_date']
	model = Assignment




class AssignmentDeleteView(View):
	
	def post(self, request, pk, assignment_id):
		assignment = get_object_or_404(Assignment,
									id=assignment_id)
		content_list = []
		for item in list(Content.objects.all()):
			newid = item.get_module_assign_content_id(assignment_id)
			if newid is not None:
				content_list.append(newid)
		assignment.delete()
		for content in content_list:
			Content.objects.get(id=content).delete()
		return redirect('course_assignment_list', pk)
	
class AssignmentGradeView(TemplateView):
	template_name = 'courses/manage/assignment/grades.html'
	assignment = None

	def get_course_grades(self):
		output = {}

		for student in self.assignment.course.students.all():
			earned_points = 0
			total_points = 0
			grade = None
			try:
				earned_points += Grade.objects.get(student = student, assignment = self.assignment).grade
				total_points += Grade.objects.get(student=student, assignment=self.assignment).assignment.points
				grade = Grade.objects.get(student = student, assignment = self.assignment).id
			except:
				earned_points = 0
				total_points = 0
			output[student] = [(get_grade(earned_points, total_points)), grade]

		return output

	def get_context_data(self, **kwargs):
		context = super(AssignmentGradeView,
						self).get_context_data(**kwargs)
		self.assignment = Assignment.objects.get(id=self.kwargs['assignment_id'])
		context['assignment'] = self.assignment
		context['studentgrades'] = self.get_course_grades()
		return context

class StudentAssignmentGrade(View):
	template_name = 'courses/manage/assignment/grade.html'
	model = Grade
	fields = ['submission_file', 'grade']
	assignment = None
	student = None

	def get_context_data(self, **kwargs):
		context = super(StudentAssignmentGrade, self).get_context_data(**kwargs)
		self.assignment = Assignment.objects.get(id=self.kwargs['assignment_id'])
		context['assignment'] = self.assignment
		self.student = User.objects.get(id=self.kwargs['student_id'])
		context['student'] = self.student
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.assignment = Assignment.objects.get(id=self.kwargs['assignment_id'])
		self.object.student = User.objects.get(id=self.kwargs['student_id'])
		self.object.save()
		return super().form_valid(form)

	def post(self,  request, *args, **kwargs):
		StudentAssignmentGrade.success_url = reverse_lazy('course_assignment_grades', kwargs={'pk': kwargs['pk'], 'assignment_id': kwargs['assignment_id']})
		return super(StudentAssignmentGrade, self).post(request, *args, **kwargs)

class StudentAssignmentGradeCreate(StudentAssignmentGrade, CreateView):
	model = Grade

class StudentAssignmentGradeUpdate(StudentAssignmentGrade, UpdateView):
	def get_object(self):
		return Grade.objects.get(student=self.kwargs['student_id'], assignment=self.kwargs['assignment_id'])


class AssignmentUpdateView(OwnerAssignmentEditMixin, UpdateView):
	def get_object(self):
		return Assignment.objects.get(id=self.kwargs['assignment_id'])
	

class CourseAssignmentList(OwnerAssignmentMixin, ListView):
	template_name = 'courses/course/assignmentList.html'
	def get_queryset(self):
		qs = super(CourseAssignmentList, self).get_queryset()
		return qs.filter(course_id=self.kwargs['pk'])	
	def get_title(self):
		return "sometext"
	def get_context_data(self, **kwargs):
		context = super(CourseAssignmentList,
						self).get_context_data(**kwargs)
		self.course = Course.objects.get(id=self.kwargs['pk'])
		context['course'] = self.course
		return context


class CourseGradeBook(TemplateView):
	template_name = 'courses/course/GradeBook.html'
	course = None

	def get_course_grades(self):
		output = {}
		for student in self.course.students.all():
			StudentGradeList = []
			earned_points = 0
			total_points = 0
			for assignment in self.course.assignments.all():
				try:
					StudentGradeList.append(get_grade(Grade.objects.get(student = student, assignment = assignment).grade, Grade.objects.get(student=student, assignment=assignment).assignment.points))

					earned_points += Grade.objects.get(student = student, assignment = assignment).grade
					total_points += Grade.objects.get(student=student, assignment=assignment).assignment.points
				except:
					StudentGradeList.append("-")
			StudentGradeList.append(get_grade(earned_points, total_points))
			output[student]=(StudentGradeList)

		return output

	def get_context_data(self, **kwargs):
		context = super(CourseGradeBook,
						self).get_context_data(**kwargs)
		self.course = Course.objects.get(id=self.kwargs['pk'])
		context['course'] = self.course
		context['studentgrades'] = self.get_course_grades()
		return context

	def get_title(self):
		return "sometext"

class CourseModuleUpdateView(TemplateResponseMixin, View):
	template_name = 'courses/manage/module/formset.html'
	course = None

	def get_formset(self, data=None):
		return ModuleFormSet(instance=self.course,
							 data=data)

	def dispatch(self, request, pk):
		self.course = get_object_or_404(Course,
										id=pk,
										owner=request.user)
		return super(CourseModuleUpdateView,
					 self).dispatch(request, pk)

	def get(self, request, *args, **kwargs):
		formset = self.get_formset()
		return self.render_to_response({'course': self.course,
										'formset': formset})

	def post(self, request, *args, **kwargs):
		formset = self.get_formset(data=request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('manage_course_list')
		return self.render_to_response({'course': self.course,
										'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
	module = None
	model = None
	obj = None
	template_name = 'courses/manage/content/form.html'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_model(self, model_name):
		if model_name in ['text', 'video', 'image', 'file', 'module_assignment', 'announcement']:
			return apps.get_model(app_label='courses',
								  model_name=model_name)
		return None

	def get_form(self, model, *args, **kwargs):
		Form = modelform_factory(model, exclude=['owner',
												 'order',
												 'created',
												 'updated'])

		return Form(*args, **kwargs)

	def dispatch(self, request, module_id, model_name, id=None):
		self.module = get_object_or_404(Module,
										id=module_id,
										course__owner=request.user)
		self.model = self.get_model(model_name)
		if id:
			self.obj = get_object_or_404(self.model,
										 id=id,
										 owner=request.user)
		return super(ContentCreateUpdateView,
					 self).dispatch(request, module_id, model_name, id)

	def get(self, request, module_id, model_name, id=None):
		form = self.get_form(self.model, instance=self.obj)
		if model_name == 'module_assignment':
			form.fields['assign'].queryset = form.fields['assign'].queryset.filter(
				course=Module.objects.get(id=self.kwargs['module_id']).getcourse().get_course_id())
		return self.render_to_response({'form': form, 'object': self.obj})

	def post(self, request, module_id, model_name, id=None):
		form = self.get_form(self.model,
							 instance=self.obj,
							 data=request.POST,
							 files=request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.owner = request.user
			obj.save()
			if not id:
				# new content
				Content.objects.create(module=self.module,
									   item=obj)
			return redirect('module_content_list', self.module.id)

		return self.render_to_response({'form': form,
										'object': self.obj})


class ContentDeleteView(View):

	def post(self, request, id):
		content = get_object_or_404(Content,
									id=id,
									module__course__owner=request.user)
		module = content.module
		content.item.delete()
		content.delete()
		return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
	template_name = 'courses/manage/module/content_list.html'

	def get(self, request, module_id):
		module = get_object_or_404(Module,
								   id=module_id,
								   course__owner=request.user)

		return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin,
					  JsonRequestResponseMixin,
					  View):
	def post(self, request):
		for id, order in self.request_json.items():
			Module.objects.filter(id=id,
								  course__owner=request.user).update(order=order)
		return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin,
					   JsonRequestResponseMixin,
					   View):
	def post(self, request):
		for id, order in self.request_json.items():
			Content.objects.filter(id=id,
								   module__course__owner=request.user) \
				.update(order=order)
		return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
	model = Course
	template_name = 'courses/course/list.html'

	def get(self, request, subject=None):
		subjects = Subject.objects.annotate(
			total_courses=Count('courses'))
		courses = Course.objects.annotate(
			total_modules=Count('modules'))
		if subject:
			subject = get_object_or_404(Subject, slug=subject)
			courses = courses.filter(subject=subject)

		return self.render_to_response({'subjects': subjects,
										'subject': subject,
										'courses': courses})


class CourseDetailView(DetailView):
	model = Course
	template_name = 'courses/course/detail.html'

	def get_context_data(self, **kwargs):
		context = super(CourseDetailView,
						self).get_context_data(**kwargs)
		context['enroll_form'] = CourseEnrollForm(
			initial={'course': self.object})
		return context

def get_grade(earned, total):
	output = "(" + str(earned) + "/" + str(total) + ") "
	if total == 0:
		output += "-"
	else:
		percent = earned/total
		if percent >= .97:
			output += "A+"
		elif percent >= .93:
			output +=  "A"
		elif percent >= .90:
			output += "A-"
		elif percent >= .87:
			output +=  "B+"
		elif percent >= .83:
			output +=  "B"
		elif percent >= .80:
			output +=  "B-"
		elif percent >= .77:
			output +=  "C+"
		elif percent >= .73:
			output +=  "C"
		elif percent >= .70:
			output +=  "C-"
		elif percent >= .67:
			output +=  "D+"
		elif percent >= .63:
			output +=  "D"
		elif percent >= .60:
			output += "D-"
		else:
			output +=  "F"
	return output

