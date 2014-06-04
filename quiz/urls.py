from django.conf.urls import patterns, url

from quiz import views

urlpatterns = patterns(
    url(r'^$', views.index, name='index'),
    url(r'^t/(?P<staff_id>\d+)/(?P<page_number>\d+)/$', views.quiz, name='quiz'),
    url(r'^forms/(?P<q_id>\d+)/$', views.forms, name='forms'),
)
