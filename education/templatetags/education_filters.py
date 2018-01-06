from django import template
import json, datetime
from django.utils import timezone
from django.db.models import Max, Sum, Count
from django.shortcuts import  get_object_or_404
from education.models import AttendanceRecord,ExamRecord, Course, Student, Exam
register = template.Library()



@register.simple_tag
def precentage_calc(first, second):
	if  second==None:
		precentage=0
		first=0
	elif first== None:
		precentage=0
		second=0
	else:		
		precentage=float("{0:.2f}".format(first/second*100))
	return precentage


@register.simple_tag
def remove_attend(attend_pk):
	return AttendanceRecord.objects.get(pk=attend_pk).delete()
 	

@register.simple_tag
def student_attend_count(student, course):
	""" Custom Template Tag that takes a student and course object and returns the count of attendances
	of the student in the specific course """
	count=AttendanceRecord.objects.filter(course=course, student=student).count()
	return count

@register.simple_tag
def course_attend_max(course):
	""" Custom Template Tag that takes a student and course object and returns the count of attendances
	of the student in the specific course """
	maxcount=course.student.filter(
            attendances__course=course).annotate(
            num_attend=Count('attendances')).aggregate(max_count=Max('num_attend'))['max_count']
	return maxcount



@register.simple_tag
def exam_records_ordered(exam):
	""" Custome Template Tag takes exam object and returns ordered queryset according to student degrees """
	records=ExamRecord.objects.filter(exam=exam).annotate(top_stud=Max('student_degree')).order_by('-top_stud')
	return records


@register.simple_tag
def student_course_exams_progress(student, course):
	""" Custom Template Tag takes a student and course object and returns a dictionary of total degrees
	of the student and course and the precentage keys are: exams, student, precentage """
	total_exams=Exam.objects.filter(course=course).aggregate(
		max_degree=Sum('max_mark'))['max_degree']
	total_student=ExamRecord.objects.for_student(
		student.pk).for_course(course.pk).aggregate(
		student_degree=Sum('student_degree'))['student_degree']
	
	if total_student!=None:
		precentage=float("{0:.2f}".format(total_student/total_exams *100))
	else:
		precentage=0
		total_student=0
	return {
		'exams':total_exams,
	 	'student':total_student,
	 	'precentage':precentage
	}


@register.simple_tag
def student_chart_exams_data(student_code, course_pk):
    course=get_object_or_404(Course, pk=course_pk)
    student=get_object_or_404(Student, code=student_code)
    records = student.examrecords.filter(exam__course=course)
    data={
    	'labels':[record.exam.name or record.exam.exam_time.strftime('%A'+' hour : '+' %H') for record in records], 
    	'data':[record.student_degree/record.exam.max_mark for record in records]
    }
    return json.dumps(data)


@register.simple_tag
def student_chart_attendances_data(student_code, course_pk):
	course=get_object_or_404(Course, pk=course_pk)
	student=get_object_or_404(Student, code=student_code)
	attendances=student.attendances.filter(course=course)
	count=attendances.count()
	days = 30
	start_date = timezone.now().today() - datetime.timedelta(days=days-1)
	datetime_list = []
	labels = []
	salesItems=[]
	for attendance in attendances:

		
		
		labels.append(
		attendance.attend_time.strftime('%A')
		)
		
	
		
	data={
	'labels':labels,
	'data':[ 1 for attendance in attendances if attendance.attend_time ]
	}
	return json.dumps(data)