from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils import timezone


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Assignment(models.Model):
	course = models.ForeignKey(Course,
							   related_name='assignments',
							   on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	description = models.TextField()
	points = models.IntegerField()
	file = models.FileField(upload_to='files',blank=True, null=True)
	due_date = models.DateTimeField(default=timezone.now,blank=True, null=True)
	
	class Meta:
		ordering = ['due_date']
	
	def __str__(self):
		return self.title

class Grade(models.Model):
	assignment = models.ForeignKey(Assignment,
							   related_name='grade',
							   on_delete=models.CASCADE)
	student = models.ForeignKey(User, related_name='student_grade',
							   on_delete=models.CASCADE)
	submission_file = models.FileField(blank=True, null=True)
	grade = models.IntegerField(blank=True, null=True)

	
	class Meta:
		ordering = ['assignment']
	
	def __str__(self):
		return assignment.title
		
	def get_grade(self):
		return self.grade

class Module(models.Model):
	course = models.ForeignKey(Course,
							   related_name='modules',
							   on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	order = OrderField(blank=True, null=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

    def is_true(self):
        check = False
        time_now = timezone.now()
        if self.release_date <= time_now:
            check = True
        return check


class Content(models.Model):
	module = models.ForeignKey(Module,
							   related_name='contents',
							   on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType,
									 on_delete=models.CASCADE,
									 limit_choices_to={'model__in': (
										 'text',
										 'video',
										 'image',
										 'file',
										 'module_assignment',
										 'announcement')})
	object_id = models.PositiveIntegerField()
	item = GenericForeignKey('content_type', 'object_id')
	order = OrderField(blank=True, for_fields=['module'])

	def get_content_id(self):
		return self.id
		
	def get_module_assign_content_id(self, assignID):
		if self.content_type.id == 10:
			 
			module_assign = self.Module_Assignment.objects.get(id=self.object_id)
			if module_assign.assign.id == assignID:
				return self.id
		return None

	class Meta:
		ordering = ['order']

	class ItemBase(models.Model):
		owner = models.ForeignKey(User,
								  related_name='%(class)s_related',
								  on_delete=models.CASCADE)
		title = models.CharField(max_length=250)
		created = models.DateTimeField(auto_now_add=True)
		updated = models.DateTimeField(auto_now=True)

		def render(self):
			return render_to_string('courses/content/{}.html'.format(
				self._meta.model_name), {'item': self})

		class Meta:
			abstract = True

		def __str__(self):
			return self.title

	class Text(ItemBase):
		content = models.TextField()

	class File(ItemBase):
		file = models.FileField(upload_to='files')

	class Image(ItemBase):
		file = models.FileField(upload_to='images')

	class Video(ItemBase):
		url = models.URLField()

	class Module_Assignment(ItemBase):
		assign = models.ForeignKey(Assignment, related_name='assignment_link', on_delete=models.CASCADE)
		
		def delete(self):
			ItemContent = Content.objects.get(id=self.id)
			ItemContent.delete()

	class Announcement(ItemBase):
		description = models.TextField()

