from django.conf.urls import patterns, url

from quiz import views

urlpatterns = patterns('',
    url(r'^forms/(?P<q_id>\d+)/$', views.forms, name='forms'),
    url(r'^form/$', views.form, name='form'),
    url(r'^jform/$', views.jform, name='jform'),
    url(r'^$', views.index, name='index'),
    url(r'^t/(?P<staff_id>\d+)/(?P<page_number>\d+)/$', views.quiz, name='quiz'),
    url(r'^ajax/test/$', views.ajax_test, name='ajax_test'),
    url(r'^mform/(?P<staff_id>\d+)/(?P<page_number>\d+)/$', views.mform, name='mform'),
)
