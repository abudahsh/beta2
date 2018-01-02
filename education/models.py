from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed

from django.dispatch import receiver
from django.db import models
import random, string, time
# Create your models here.
from django.urls import reverse
from .managers import ExamRecordManager

codes=[]
def id_generator(size=5, chars=string.ascii_uppercase + 4*string.digits):
    x= (''.join(random.choice(chars) for i in range(size)))
    if codes.__contains__(x):
        return id_generator()
    codes.append(x)
    return x

class BaseUser(AbstractBaseUser):

    def get_student(self):
        try:
            return self.student
        except:
            return False

    def get_teacher(self):
        try:
            return self.school
        except:
            return False


class Student(models.Model):
    user = models.OneToOneField(User)
    study_at=models.CharField(max_length=70, null=True, blank=True)
    code = models.CharField(max_length=5, null=False, primary_key=True, default=id_generator)



    def __str__(self):
        return self.user.username


class School(models.Model):
    user=models.OneToOneField(User)
    Name=models.CharField(max_length=50, null=False)
    adress=models.TextField(max_length=120)
    photo=models.ImageField(blank=True)
    bio=models.TextField(max_length=500)
    slug=models.SlugField(max_length=20)

    class Meta:
        permissions = (
            ("add_students", "Can add new students"),
            ("edit_course", "Can change the information of course"),
            ("delete_student", "Can remove a student by setting its status as closed"),
        )
    def __str__(self):
        return self.Name

class Course(models.Model):
    years=(
        ('a', 'اولي اعدادي'),
        ('b', 'ثانية اعدادي'),
        ('c', 'ثالتة اعدادي'),
        ('d', 'اولي ثانوي'),
        ('e', 'ثانية ثانوي'),
        ('f', 'ثالثة ثانوي'),
        ('g', 'اخري'),
    )
    name=models.CharField(max_length=50, null=False)
    photo = models.ImageField(blank=True)
    groups=models.TextField(null=True)
    school=models.ForeignKey(School)
    year=models.CharField(max_length=30,choices=years)
    student=models.ManyToManyField(Student , related_name='students')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('edu:course_dashboard', args=[self.id])


class Exam(models.Model):
    course=models.ForeignKey(Course, related_name='exams')
    name=models.CharField(max_length=60, null=True, blank=True)
    exam_time=models.DateTimeField(auto_now_add=True,auto_now=False, editable=True)
    max_mark=models.FloatField()

    def __str__(self):
        if self.name:
            return self.name
        return 'Exam of course '+str(self.course.name)+' at time '+(self.exam_time).strftime('%A,  %I:%M %p, %d, %B')

class ExamRecord(models.Model):
    exam=models.ForeignKey(Exam, related_name='examrecords')
    exam_time=models.DateTimeField(auto_now_add=True,auto_now=False, editable=True)
    student_degree=models.FloatField()
    student=models.ForeignKey(Student, related_name='examrecords')
   
    objects=ExamRecordManager()

    class Meta:
        unique_together=['exam', 'student']

    def __str__(self):
        return str(self.student) +' got ' +str(self.student_degree) + ' on Exam' +' from '+str(self.exam.max_mark)

class AttendanceRecord(models.Model):
    course=models.ForeignKey(Course, related_name='records')
    student = models.ForeignKey(Student, related_name='attendances')
    attend_time=models.DateTimeField(auto_now_add=True,auto_now=False, editable=True)
    update=models.DateTimeField(auto_now_add=False,auto_now=True, editable=True)


    def __str__(self):
        return (self.attend_time).strftime('%A,  %I:%M %p, %d, %B') + '  ' +str( self.student)


class Notification(models.Model):
    course=models.ForeignKey(Course ,related_name='notifications')
    text=models.CharField(max_length=300)
    time_stamp=models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=False, auto_now=True, editable=True)

    def __str__(self):
        return self.text


class Question(models.Model):
    course=models.ForeignKey(Course, related_name='questions')
    title=models.CharField(max_length=150)
    description=models.TextField( null=True, blank=True)
    image=models.ImageField(blank=True, null=True)
    time_stamp=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now_add=False, auto_now=True)
    asker=models.ForeignKey(Student, related_name='questions')
    def __str__(self):

        return self.title


class Reply(models.Model):
    question=models.ForeignKey(Question, related_name='replies')
    text=models.TextField()
    image=models.ImageField(null=True, blank=True)
    replier=models.ForeignKey(Student, related_name='replies')
    likes=models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return self.text

class StudentReport(models.Model):
    course=models.ForeignKey(Course, related_name='reports')
    student=models.ForeignKey(Student, related_name='reports')
    exams=models.ManyToManyField(Exam, blank=True)
    examrecords=models.ManyToManyField(ExamRecord, blank=True)
    attendances=models.ManyToManyField(AttendanceRecord, blank=True)
    total_student_degrees=models.PositiveIntegerField(blank=True, default=0, null=True)
    total_max_exam_degrees=models.PositiveIntegerField(blank=True, default=0, null=True)
    total_attendance_score=models.PositiveIntegerField(blank=True, default=0, null=True)

    class Meta:
        unique_together=['course', 'student']

    def __str__(self):
        return 'Report of Student: ' + str(self.student)


def update_report_exams(sender, instance, **kwargs):
    exams=instance.exams.filter(course=instance.course)
    total_exams=0
    for exam in exams:
        total_exams+=exam.max_mark
       
    instance.total_max_exam_degrees=total_exams
    instance.save()



def update_report_examrecords(sender, instance, **kwargs):
    exam_set=instance.exams.all()
    examrecords=instance.examrecords.filter(student=instance.student, exam__in=exam_set)
    total_student=0
    for record in examrecords:
        total_student+=record.student_degree
    instance.total_student_degrees = total_student
    instance.save()

def update_report_attendances(sender, instance, **kwargs):
    instance.total_attendance_score=instance.attendances.filter(student=instance.student).count()
    instance.save()





m2m_changed.connect(update_report_exams, sender=StudentReport.exams.through)
m2m_changed.connect(update_report_examrecords, sender=StudentReport.examrecords.through)
m2m_changed.connect(update_report_attendances, sender=StudentReport.attendances.through)