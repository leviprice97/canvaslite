from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum


def home_view_public(request):
    return render(request, 'lms/home_view_public.html',
                  {'lms': home_view_public})

def assignment_new(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_date = timezone.now()
            assignment.save()
            assignments = Assignment.objects.filter(created_date__lte=timezone.now())
            return render(request, 'lms/assignment_list.html',
                          {'assignments': assignments})
    else:
        form = AssignmentForm()
        # print("Else")
    return render(request, 'lms/assignment_new.html', {'form': form})


def course_new(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_date = timezone.now()
            course.save()
            courses = Course.objects.filter(created_date__lte=timezone.now())
            return render(request, 'lms/course_list.html',
                          {'courses': courses})
    else:
        form = CourseForm()
        # print("Else")
    return render(request, 'lms/course_new.html', {'form': form})


def course_list(request):
    courses = Course.objects.filter(created_date__lte=timezone.now())
    return render(request, 'lms/course_list.html', {'courses': courses})


def assignment_list(request):
    assignments = Assignment.objects.filter(created_date__lte=timezone.now())
    return render(request, 'lms/assignment_list.html', {'assignments': assignments})


def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save()
            # service.customer = service.id
            assignment.updated_date = timezone.now()
            assignment.save()
            assignments = Assignment.objects.filter(created_date__lte=timezone.now())
            return render(request, 'lms/assignment_list.html', {'assignments': assignments})
    else:
        # print("else")
        form = AssignmentForm(instance=assignment)
    return render(request, 'lms/assignment_edit.html', {'form': form})


def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    assignment.delete()
    return redirect('lms:assignment_list')


def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            # service.customer = service.id
            course.updated_date = timezone.now()
            course.save()
            courses = Course.objects.filter(created_date__lte=timezone.now())
            return render(request, 'lms/course_list.html', {'courses': courses})
    else:
        # print("else")
        form = CourseForm(instance=course)
    return render(request, 'lms/course_edit.html', {'form': form})


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('lms:course_list')
	

def announcement_list(request):
    announcement = Announcement.objects.filter(created_date__lte=timezone.now())
    return render(request, 'lms/announcement_list.html', {'announcements': announcements})
	
def announcement_view_public(request):
    announcement = Announcement.objects.filter(created_date__lte=timezone.now())
    return render(request, 'lms/announcement_view_public.html', {'announcements': announcements})
	
def announcement_view_instructor(request):
    announcement = Announcement.objects.filter(created_date__lte=timezone.now())
    return render(request, 'lms/announcement_view_instructor.html', {'announcements': announcements})

def announcement_create_instructor(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_date = timezone.now()
            service.save()
            announcements = Announcement.objects.filter(created_date__lte=timezone.now())
            return render(request, 'lms/announcement_list.html',
                          {'announcements': announcements})
    else:
        form = AnnouncementForm()
        # print("Else")
    return render(request, 'lms/announcement_create_instructor.html', {'form': form})

def announcement_edit_instructor(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            announcement = form.save()
            # service.customer = service.id
            announcement.updated_date = timezone.now()
            announcement.save()
            announcements = Announcement.objects.filter(created_date__lte=timezone.now())
            return render(request, 'lms/announcement_list.html', {'announcements': announcements})
    else:
        # print("else")
        form = AnnouncementForm(instance=announcement)
    return render(request, 'lms/announcement_edit_instructor', {'form': form})

def announcement_delete_instructor(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    return redirect('lms:announcement_list')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lms:file_list')
    else:
        form = DocumentForm()
    return render(request, 'lms/model_form_upload.html', {
        'form': form
    })


def file_list(request):
    files = Document.objects.all()
    return render(request, 'lms/file_list.html',
                  {'files': files})


def delete_file(request, pk):
    file = get_object_or_404(Document, pk=pk)
    file.delete()
    return redirect('lms:file_list')
