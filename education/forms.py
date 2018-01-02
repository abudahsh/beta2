from django import forms

from education.models import Course, Student, AttendanceRecord, Exam, ExamRecord


class AddingStudentForm(forms.ModelForm):

    class Meta:
        model= Course
        fields=['student']


class CreateStudentForm(forms.ModelForm):

    class Meta:
        model= Student
        fields=['study_at', 'code']


class TakeAttendForm(forms.ModelForm):
	"""docstring for TakeAttendForm"""
	code=forms.CharField()
	class Meta:
		model= AttendanceRecord
		fields = ["code"]

class CreateExamForm(forms.ModelForm):
    """docstring for ClassName"""
    class Meta:
        model=Exam
        fields=['name','max_mark']

class ExamRecordForm(forms.ModelForm):

    code=forms.CharField()

    class Meta:
        model=ExamRecord
        fields=['code','student_degree']


class AttendanceFilterForm(forms.Form):
    From=forms.DateTimeField()
    To=forms.DateTimeField()
    