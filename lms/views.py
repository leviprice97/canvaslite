from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum


def assignment_new(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_date = timezone.now()
            service.save()
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
