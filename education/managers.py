from django.db import models


class ExamRecordsQuerySet(models.QuerySet):

    def for_student(self, student_pk):
        return self.filter(student__pk=student_pk)

    def for_course(self, course_pk):
        return self.filter(exam__course__pk=course_pk)
        
class ExamRecordManager(models.Manager):

    def get_queryset(self):
        return ExamRecordsQuerySet(self.model, using=self._db)  # Important!

    def for_student(self, student_pk):
        return self.get_queryset().for_student(student_pk)

    def for_course(self, size):
        return self.get_queryset().for_course(course_pk)