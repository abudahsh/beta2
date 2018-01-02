from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404

from education.models import Course, School

class BaseUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return True


class DashboardPermissionMixin(BaseUserPassesTestMixin):
    raise_exception = True
    requires_login = False

    def test_func(self):
        if not self.request.user.is_authenticated():
            self.requires_login = True
            return False

        if not self.request.user.school:
            return False
            '''
        if not (self.request.user.get_student() or
                self.request.user.get_teacher() or
                self.request.user.is_superuser):
            return False
            '''
        return True and super().test_func()

    def handle_no_permission(self):
        if self.requires_login:
            return redirect_to_login(
                self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

        return super().handle_no_permission()


class DashboardPermissionMixin(BaseUserPassesTestMixin):
    raise_exception = True
    requires_login = False

    def test_func(self):
        if not self.request.user.is_authenticated():
            self.requires_login = True
            return False

        if not self.request.user.school:
            return False
            '''
        if not (self.request.user.get_student() or
                self.request.user.get_teacher() or
                self.request.user.is_superuser):
            return False
            '''
        return True and super().test_func()

    def handle_no_permission(self):
        if self.requires_login:
            return redirect_to_login(
                self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

        return super().handle_no_permission()

class CannotSeeOtherStudentsMixin(BaseUserPassesTestMixin):
    '''
    If teacher is not part of the course teachers, he cannot see
    the students detailed information
    '''
    def test_func(self):
        course_id = self.kwargs.get('course')
        course = get_object_or_404(Course, pk=course_id)
        school = School.objects.filter(id=self.request.user.id,
                                         teached_courses__id__exact=course.id)
        if not school.exists():
            return False

        ca_id = self.kwargs.get('ca')
        #ca = CourseAssignment.objects.filter(id=ca_id, course=course_id)
        if not course.exists():
            return False

        return True and super().test_func()

class TeacherCannotSeeOtherCoursesDashboardMixin(BaseUserPassesTestMixin):
    """to forbid schools from accessing each other's courses by me"""
    raise_exception = True
    requires_login = False
    def test_func(self):
        course_id = self.kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_id)
        if course.school == self.request.user.school:
            return True and super().test_func()
        else:
            return False

    
        
class CannotSeeOthersCoursesDashboardsMixin(BaseUserPassesTestMixin):
    def test_func(self):
        course_id = self.kwargs.get('course')
        course = get_object_or_404(Course, pk=course_id)
        #qs = CourseAssignment.objects.filter(user=self.request.user, course=course)
        school = School.objects.filter(id=self.request.user.id,
                                         teached_courses__id__exact=course.id)

        if not course.exists() and not school.exists():
            return False

        self.course = course
        return True and super().test_func()


class IsTeacherMixin(BaseUserPassesTestMixin):
    def test_func(self):
        if not self.request.user.get_teacher():
            return False

        return True and super().test_func()


class IsStudentMixin(BaseUserPassesTestMixin):
    def test_func(self):
        if not self.request.user.get_student():
            return False

        return True and super().test_func()



class CannotSeeCourseTaskListMixin(BaseUserPassesTestMixin):
    def test_func(self):
        if not self.course.task_set.exists():
            raise Http404

        return True and super().test_func()


class IsDateInDeadlineDateForCourse(BaseUserPassesTestMixin):
    def test_func(self):
        if not self.course.is_in_deadline():
            raise Http404

        return True and super().test_func()
