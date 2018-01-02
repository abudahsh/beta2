from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView, logout

from accounts.views import registeration

urlpatterns = [

    url(r'^login/', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^register/', registeration, name='register'),
]