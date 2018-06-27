from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
import datetime
from django.db.models import Max, Sum, Count, Q
from django.http import JsonResponse
# Create your views here.
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView, DetailView, CreateView, View

from education.forms import AddingStudentForm, CreateStudentForm, TakeAttendForm, ExamRecordForm, CreateExamForm,AttendanceFilterForm
from education.mixins import  TeacherCannotSeeOtherCoursesDashboardMixin
from education.models import Course, Student, AttendanceRecord, Exam, ExamRecord, Question,Notification,StudentReport




class CourseViewForSchool(TemplateView):
    """ The view of the course for a School viewer"""
    template_name = 'school_course_dashboard.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        context['course']=course=get_object_or_404(Course, pk=self.kwargs['course_pk'])
        attendances = AttendanceRecord.objects.filter(course=course)

        context['attendances'] = attendances
        context['students']= students=course.student.filter(
            attendances__course=course).annotate(
            num_attend=Count('attendances')).order_by('-num_attend')
        context['top_attend']=course.student.filter(
            attendances__course=course).annotate(
            num_attend=Count('attendances')).aggregate(Max('num_attend'))
        context['records']=ExamRecord.objects.filter(
            exam__course=course).annotate(
            top_stud=Max('student_degree')).order_by('-top_stud')
        context['form']=TakeAttendForm
        context['form2']=CreateExamForm
        return context









class AddingStudentView(FormView):
    template_name = 'adding_student.html'
    form_class = AddingStudentForm
    success_url = reverse_lazy('edu:signed_home')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        form.instance.name=course.name
        form.instance.school = course.school
        form.instance.year = course.year
        form.instance.pk = course.pk
        #form['student'] = course.student
        return form



class TakeStudentAttendance(FormView):
    """docstring for ClassName"""

    form_class=TakeAttendForm
    template_name='take_attend.html'
    success_url=reverse_lazy('edu:not_signed_home')
    def form_valid(self, form):
        course=get_object_or_404(Course, pk=self.kwargs['course_pk'])
        form.instance.course=course
        code=form.cleaned_data.get('code')
        form.instance.student=Student.objects.get(code=code)
        return super(TakeStudentAttendance, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['course']=course=get_object_or_404(Course, pk=self.kwargs['course_pk'])
        return context


def take_attend(request, course_pk):
    """ The Fucntion that handles the take attendance form that appears in SchoolCourseDashboard """
    course=get_object_or_404(Course, pk=course_pk)

    if request.method == 'POST':
        form=TakeAttendForm(request.POST)

        if form.is_valid():
            attend=form.save(commit=False)
            student_code=form.cleaned_data.get('code')
            attend.student=student=Student.objects.get(code=student_code)
            if not get_object_or_404(Course, student__code=student_code, pk=course_pk):
                return redirect("Not foooond")
            attend.course=course
            attend.save()
            return redirect('edu:course_dashboard', course_pk=course_pk)
    else:
        form=TakeAttendForm()
    return render(request, 'school_course_dashboard.html', {'form': form, 'course':course})


def create_exam(request, course_pk):
    """ The fucntion that handles creating exam form that appears in SchoolCourseDashboard """

    course=get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        form=CreateExamForm(request.POST)
        if form.is_valid():
            exam=form.save(commit=False)
            exam.course=course
            exam.name=form.cleaned_data['name']
            exam.max_mark=form.cleaned_data['max_mark']
            exam.save()
            return redirect('edu:course_dashboard', course_pk=course_pk)
    else:
        form=CreateExamForm()
    return render(request, 'school_course_dashboard.html', {'form2': form, 'course':course})




def create_exam_record(request, course_pk, exam_pk):
    """ The function that handling creating exam records that appears in ??????"""
    course=get_object_or_404(Course, pk=course_pk)
    exam=get_object_or_404(Exam, pk=exam_pk)

    if request.method =='POST':
        form=ExamRecordForm(request.POST)
        if form.is_valid():
            record=form.save(commit=False)
            student_code=form.cleaned_data.get('code')
            record.student=Student.objects.get(code=student_code)
            record.exam=exam
            record.student_degree=form.cleaned_data.get('student_degree')

            record.save()
            return redirect('edu:exam_detail', course_pk=course_pk, exam_pk=exam_pk)

        form=ExamRecordForm()
    return render(request, 'school_exam_dashboard.html', {'form': form, 'course':course})


class SchoolExamDashboardView(TemplateView):
    template_name='school_exam_dashboard.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['course']=course=get_object_or_404(Course, pk=self.kwargs['course_pk'])
        context['exam']=exam=get_object_or_404(Exam, pk=self.kwargs['exam_pk'])
        context['form']= ExamRecordForm
        context['students']=students=Student.objects.filter(courses=course)
        context['exams']=Exam.objects.annotate(top_stud=Max('examrecords__student_degree'))
        return context
