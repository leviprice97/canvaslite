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
