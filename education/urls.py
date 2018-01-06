from django.conf.urls import url

from education import views

urlpatterns = [
    url(r'^t/$', views.AllCoursesList.as_view(), name='not_signed_home'),
    url(r'^s/$', views.StudentCourses.as_view(), name='signed_home'),
    url(r'^student/create/$', views.UserCreateStudentView.as_view(), name='create_student'),
    url(r'^template/$', views.Template.as_view(), name='template'),
    url(r'^(?P<student_code>\w+)/$', views.StudentAllCoursesState.as_view(), name='student_all_courses_state'),
    url(r'^course/(?P<course_pk>\d+)/add/$', views.AddingStudentView.as_view(), name='adding_student'),
    url(r'^course/(?P<course_pk>\d+)/take/$', views.take_attend, name='take_attend'),
    url(r'^course/(?P<course_pk>\d+)/exam/create/$', views.create_exam, name='create_exam'),
    url(r'^course/(?P<course_pk>\d+)/exam/(?P<exam_pk>\d+)/create/$', views.create_exam_record, name='create_exam_record'),    
    url(r'^course/(?P<course_pk>\d+)/exam/(?P<exam_pk>\d+)/$', views.SchoolExamDashboardView.as_view(), name='exam_detail'),
    url(r'^course/(?P<course_pk>\d+)/(?P<student_code>\w+)/report/', views.StudentCourseReport.as_view(),name='student_course_report'),
    url(r'^course/(?P<course_pk>\d+)/(?P<student_code>\w+)/', views.StudentCourseInfoView.as_view(),name='student_course_info'),
    url(r'^course/(?P<course_pk>\d+)/(?P<student_code>\w+)/ajax/', views.StudentAjaxCourseView,name='student_course_info_ajax'),
    url(r'^course/(?P<course_pk>\d+)/$', views.CourseViewForSchool.as_view(), name='course_dashboard'),
    url(r'^course/(?P<course_pk>\d+)/s$', views.CourseViewForParticipant.as_view(), name='course_dashboard_participant'),
]