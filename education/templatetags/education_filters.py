from django import template
from  education.models import AttendanceRecord,ExamRecord
register = template.Library()



@register.simple_tag
def remove_attend(attend_pk):
	return AttendanceRecord.objects.get(pk=attend_pk).delete()
 	

@register.simple_tag
def student_attend_count(student, course):
	count=AttendanceRecord.objects.filter(course=course, student=student).count()
	return count