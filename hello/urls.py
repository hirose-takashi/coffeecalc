from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.hello_world, name='hello_world'),
    url(r'^template/$', views.hello_template, name='hello_template'),
    url(r'^if/$', views.hello_if, name='hello_if'),
    url(r'^for/$', views.hello_for, name='hello_for'),
    url(r'^get/$', views.hello_get_query, name='hello_get_query'),
    url('/hello/', views.hello_form_post, name='hello_form_post'),
]
