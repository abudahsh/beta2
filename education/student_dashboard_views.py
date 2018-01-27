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



class StudentCourses(ListView):
    template_name = 'edu_index_signed.html'
    context_object_name = 'courses'
    def get_queryset(self):
        queryset = Course.objects.filter(student=self.request.user.student)
        return queryset

class CourseViewForParticipant(TemplateView):
    """ The view of the course for a student viewer"""
    template_name='participant_course_view.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['course']=course=get_object_or_404(Course, pk=self.kwargs['course_pk'])
        context['questions']=Question.objects.filter(course=course)
        context['notifications']=Notification.objects.filter(course=course)
        return context




class StudentCourseInfoView(TemplateView):

    template_name = 'student_course_info.html'

    def get_context_data(self, **kwargs):
        total_student=0
        total_max=0
        context=super().get_context_data(**kwargs)
        context['course']=course=get_object_or_404(Course, pk=self.kwargs['course_pk'])
        context['student']=student = get_object_or_404(Student, code=self.kwargs['student_code'])
        context['attendances']=AttendanceRecord.objects.filter(course=course, student=student)
        context['exams']=exams=Exam.objects.filter(course=course)

        for k,vals in self.request.GET.lists():
            for v in vals:
                context['attendances']=AttendanceRecord.objects.filter(
                    course=course, student=student).filter( Q(attend_time__gte=v))
                context['exams']=exams=Exam.objects.filter(course=course ,exam_time__gte=v)
                records=ExamRecord.objects.filter(
                    student=student).filter(
                    exam__course=course ,exam__exam_time__gte=v).annotate(
                    top_stud=Max('student_degree')).order_by('-top_stud')
                context['exam_records']=records
                context['aggregate_student']=ExamRecord.objects.for_student(
                    student.pk).for_course(course.pk).filter(
                    exam__exam_time__gte=v).aggregate(student_degree=Sum('student_degree'))
                context['aggregate_exams']=Exam.objects.filter(course=course ,exam_time__gte=v).aggregate(
                    Max_Degree=Sum('max_mark'))
                return context

        records=ExamRecord.objects.filter(student=student).filter(
            exam__course=course).annotate(
            top_stud=Max('student_degree')).order_by('-top_stud')
        context['exam_records']=records
        context['aggregate_student']=ExamRecord.objects.for_student(student.pk).for_course(course.pk).aggregate(
            student_degree=Sum('student_degree'))
        context['aggregate_exams']=Exam.objects.filter(course=course).aggregate(Max_Degree=Sum('max_mark'))
        context['form']=AttendanceFilterForm
        return context






class StudentAllCoursesState(TemplateView):
    template_name = 'student_all_courses_state.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['student']=student = get_object_or_404(Student, code=self.kwargs['student_code'])
        context['courses']=courses=Course.objects.filter(student=student)
        return context



class StudentCourseReport(TemplateView):

    template_name='student_course_report.html'
    context_object_name='report'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['report']=get_object_or_404(StudentReport,
        course=self.kwargs['course_pk'],
        student=self.kwargs['student_code'])
        return context



class AttendanceJsonView(View):
    template_name='attend_json.html'
    def get(self, request, *args, **kwargs):
        student=get_object_or_404(Student, code=self.kwargs['student_code'])
        course=get_object_or_404(Course, pk=self.kwargs['course_pk'])
        attendances=AttendanceRecord.objects.filter(student=student, course=course)
        attendances_list=[]
        attendance_count=attendances.count()
        for attend in (attendances):
            attendances_list.append(attend.attend_time)
        data={
        'student':student.user.username,
        'course':course.name,
        'attendances':attendances_list,
        'attend_count':attendance_count
        }
        return JsonResponse(data)


class StudentCoursesAttendancesJsonView(View):
    def get(self, request, *args, **kwargs):
        student=get_object_or_404(Student, code=self.kwargs['student_code'])
        courses=Course.objects.filter(student=student)
        courses_attendances=[]
        for course in courses:
            attendances=AttendanceRecord.objects.filter(student=student, course=course)
            attendances_list=[]
            attendance_count=attendances.count()
            for attend in (attendances):
                attendances_list.append(attend.attend_time)
            courses_attendances.append(attendances_list)
        data={
        'student':student.user.username,
        'courses':{
        'course':[course.name for course in courses],
        'course_attend':[course_attendance for course_attendance in courses_attendances],
        }
        }
        return JsonResponse(data)
