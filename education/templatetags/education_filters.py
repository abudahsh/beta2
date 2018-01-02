from django import template
from django.db.models import Max, Sum, Count
from  education.models import AttendanceRecord,ExamRecord
register = template.Library()



@register.simple_tag
def remove_attend(attend_pk):
	return AttendanceRecord.objects.get(pk=attend_pk).delete()
 	

@register.simple_tag
def student_attend_count(student, course):
	count=AttendanceRecord.objects.filter(course=course, student=student).count()
	return count



@register.simple_tag
def exam_records_ordered(exam):
	records=ExamRecord.objects.filter(exam=exam).annotate(top_stud=Max('student_degree')).order_by('-top_stud')
	return records