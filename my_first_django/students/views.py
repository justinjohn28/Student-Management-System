# Inside students/views.py

from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

def student_list(request):
    students = Student.objects.all()

    query = request.GET.get('q', '')
    course = request.GET.get('course')
    gender = request.GET.get('gender')
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')

    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    if course:
        students = students.filter(course__iexact=course)
    if gender:
        students = students.filter(gender__iexact=gender)
    if age_min and age_max:
        students = students.filter(age__gte=age_min, age__lte=age_max)

    return render(request, 'students/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})

def edit_student(request, id):
    student = get_object_or_404(Student, pk=id)  # Fetch the student or return 404 if not found
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)  # Pass instance to form
        if form.is_valid():
            form.save()
            return redirect('student_list')  # Redirect to the student list after saving
    else:
        form = StudentForm(instance=student)  # Initialize form with student instance on GET request
    return render(request, 'students/edit_student.html', {'form': form, 'student': student})

def delete_student(request, id):
    student = get_object_or_404(Student, pk=id)
    student.delete()
    # Redirect to the student list page or another appropriate page
    return redirect('student_list')  # Ensure 'student_list' is the correct name for the list view