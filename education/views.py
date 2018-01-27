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

class Template(TemplateView):
    template_name='testo.html'


class AllCoursesList(ListView):
    model = Course
    template_name = 'edu_index_not_signed.html'
    context_object_name = 'courses'


class UserCreateStudentView(CreateView):
    form_class = CreateStudentForm
    template_name = 'create_student.html'
    success_url = reverse_lazy('edu:not_signed_home')
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(UserCreateStudentView, self).form_valid(form)
