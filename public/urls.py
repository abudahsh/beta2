from django.conf.urls import url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST

from public import views

urlpatterns = [

    url(r'^/', views.home, name='home'),

    url(r'^products/', views.ProductListView.as_view(), name='product_list'),
    url(r'^service/(?P<pk>\d+)/', views.ServiceDetail.as_view(), name='service_detail'),
    url(r'^service/up/(?P<pk>\d+)/', views.ServiceUpdate.as_view(), name='service_update'),
    url(r'^service/add/', views.ServiceCreation.as_view(), name='service_creation'),
    url(r'^product/add/', views.ProductCreation.as_view(), name='product_creation'),
    url(r'^product/(?P<pk>\d+)/', views.ProductDetail.as_view(), name='product_detail'),
    #url(r'^review/', require_POST(views.ReviewCreation.as_view()), name='review_creation'),
    url(r'^review/p/', views.product_review_form, name='product_review_creation'),
    url(r'^review/s/', views.service_review_form, name='service_review_creation'),

]