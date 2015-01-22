from django.conf.urls import patterns, url

from quiz import views

urlpatterns = patterns('',
    url(r'^forms/(?P<q_id>\d+)/$', views.forms, name='forms'),
    url(r'^form/$', views.form, name='form'),
    url(r'^jform/$', views.jform, name='jform'),
    url(r'^$', views.index, name='index'),
    url(r'^ajax/test/$', views.ajax_test, name='ajax_test'),
    url(r'^ajax/test2/$', views.ajax_test2, name='ajax_test2'),
    url(r'^t/(?P<staff_id>\d+)/(?P<question_id>\d+)/$', views.quiz, name='quiz'),
    url(r'^end/$', views.end, name='end'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^report/(?P<staff_id>\d+)/$', views.report, name='report'),
)
