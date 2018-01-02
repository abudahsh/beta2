from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
import datetime
from django.db.models import Max, Sum, Count, Q
# Create your views here.

from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView, DetailView, CreateView

from education.forms import AddingStudentForm, CreateStudentForm, TakeAttendForm, ExamRecordForm, CreateExamForm,AttendanceFilterForm
from education.mixins import  TeacherCannotSeeOtherCoursesDashboardMixin
from education.models import Course, Student, AttendanceRecord, Exam, ExamRecord, Question,Notification,StudentReport

class Template(TemplateView):
    template_name='testo.html'


class AllCoursesList(ListView):
    model = Course
    template_name = 'edu_index_not_signed.html'
    context_object_name = 'courses'

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


class CourseViewForSchool(TemplateView):
    """ The view of the course for a School viewer"""
    template_name = 'school_course_dashboard.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)


        context['course']=course=get_object_or_404(Course, pk=self.kwargs['course_pk'])
        attendances = AttendanceRecord.objects.filter(course=course)

        context['attendances'] = attendances
        context['students']= students=course.student.filter(attendances__course=course).annotate(num_attend=Count('attendances')).order_by('-num_attend')
        context['top_attend']=course.student.filter(attendances__course=course).annotate(num_attend=Count('attendances')).aggregate(Max('num_attend'))
        context['records']=ExamRecord.objects.filter(exam__course=course).annotate(top_stud=Max('student_degree')).order_by('-top_stud')
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
                context['attendances']=AttendanceRecord.objects.filter(course=course, student=student).filter( Q(attend_time__gte=v))
                context['exams']=exams=Exam.objects.filter(course=course ,exam_time__gte=v)
                records=ExamRecord.objects.filter(student=student).filter(exam__course=course ,exam__exam_time__gte=v).annotate(top_stud=Max('student_degree')).order_by('-top_stud')
                context['exam_records']=records
                context['aggregate_student']=ExamRecord.objects.for_student(student.pk).for_course(course.pk).filter(exam__exam_time__gte=v).aggregate(student_degree=Sum('student_degree'))
                context['aggregate_exams']=Exam.objects.filter(course=course ,exam_time__gte=v).aggregate(Max_Degree=Sum('max_mark'))
                return context
        
        records=ExamRecord.objects.filter(student=student).filter(exam__course=course).annotate(top_stud=Max('student_degree')).order_by('-top_stud')
        context['exam_records']=records
        context['aggregate_student']=ExamRecord.objects.for_student(student.pk).for_course(course.pk).aggregate(student_degree=Sum('student_degree'))
        context['aggregate_exams']=Exam.objects.filter(course=course).aggregate(Max_Degree=Sum('max_mark'))
        context['form']=AttendanceFilterForm
        return context
        
        
        

class UserCreateStudentView(CreateView):
    form_class = CreateStudentForm
    template_name = 'create_student.html'
    success_url = reverse_lazy('edu:not_signed_home')
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(UserCreateStudentView, self).form_valid(form)


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


class StudentAllCoursesState(TemplateView):
    template_name = 'student_all_courses_state.html'

    def get_context_data(self, **kwargs):
        total_student=0
        total_max=0
        context=super().get_context_data(**kwargs)
        context['total_student']=total_student
        context['student']=student = get_object_or_404(Student, code=self.kwargs['student_code'])
        context['courses']=courses=Course.objects.filter(student=student)
        for course in courses:
            context['attendances']=AttendanceRecord.objects.filter(course=course, student=student)
            context['exams']=exams=Exam.objects.filter(course=course)
            context['exam_records']=records=ExamRecord.objects.for_student(student.pk).for_course(course.pk)
            context['aggregate']=ExamRecord.objects.for_student(student.pk).for_course(course.pk).aggregate(Sum('student_degree'))
        return context



class StudentCourseReport(TemplateView):
    
    template_name='student_course_report.html'
    context_object_name='report'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['report']=get_object_or_404(StudentReport, course=self.kwargs['course_pk'], student=self.kwargs['student_code'])
        return context