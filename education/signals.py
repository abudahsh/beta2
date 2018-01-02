from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import StudentReport


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