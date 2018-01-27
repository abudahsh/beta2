from django.conf.urls import url, include
from education import school_dashboard_views as school_views
from education import student_dashboard_views as student_views
from education import views



student_urlpattern=[

    url(r'^s/$', student_views.StudentCourses.as_view(), name='signed_home'),

    url(r'^(?P<student_code>\w+)/$', student_views.StudentAllCoursesState.as_view(), name='student_all_courses_state'),
    url(r'^course/(?P<course_pk>\d+)/(?P<student_code>\w+)/report/', student_views.StudentCourseReport.as_view(),name='student_course_report'),
    url(r'^course/(?P<course_pk>\d+)/(?P<student_code>\w+)/', student_views.StudentCourseInfoView.as_view(),name='student_course_info'),
    url(r'^course/(?P<course_pk>\d+)/s$', student_views.CourseViewForParticipant.as_view(), name='course_dashboard_participant'),
]

school_urlpattern=[
    url(r'^course/(?P<course_pk>\d+)/add/$', school_views.AddingStudentView.as_view(), name='adding_student'),

    url(r'^course/(?P<course_pk>\d+)/exam/(?P<exam_pk>\d+)/$', school_views.SchoolExamDashboardView.as_view(), name='exam_detail'),
    url(r'^course/(?P<course_pk>\d+)/$', school_views.CourseViewForSchool.as_view(), name='course_dashboard'),




    url(r'^course/(?P<course_pk>\d+)/take/$', school_views.take_attend, name='take_attend'),
    url(r'^course/(?P<course_pk>\d+)/exam/create/$', school_views.create_exam, name='create_exam'),
    url(r'^course/(?P<course_pk>\d+)/exam/(?P<exam_pk>\d+)/create/$', school_views.create_exam_record, name='create_exam_record'),


    url(r'^course/(?P<course_pk>\d+)/(?P<student_code>\w+)/json/', student_views.AttendanceJsonView.as_view(),name='student_attend_json'),
    url(r'^course/(?P<student_code>\w+)/json/', student_views.StudentCoursesAttendancesJsonView.as_view(),name='student_attend_json'),

]
general_urlpattern=[
    url(r'^template/$', views.Template.as_view(), name='template'),
    url(r'^student/create/$', views.UserCreateStudentView.as_view(), name='create_student'),
    url(r'^t/$', views.AllCoursesList.as_view(), name='not_signed_home'),

]

urlpatterns= [
url(r'^st/',include(student_urlpattern)),
url(r'^sc/',include(school_urlpattern)),
url(r'^',include(general_urlpattern)),
]
