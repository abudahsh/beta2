from django.contrib import admin
from .models import BaseUser, Student, School, Course,AttendanceRecord,ExamRecord,Notification,Exam,Question,Reply,StudentReport
# Register your models here.
admin.site.register(BaseUser)
admin.site.register(Student)
admin.site.register(School)
admin.site.register(Course)
admin.site.register(AttendanceRecord)
admin.site.register(Exam)
admin.site.register(ExamRecord)
admin.site.register(Notification)
admin.site.register(Question)
admin.site.register(Reply)
admin.site.register(StudentReport)
