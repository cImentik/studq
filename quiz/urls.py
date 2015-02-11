from django.conf.urls import patterns, url

from quiz import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^t/(?P<staff_id>\d+)/(?P<question_id>\d+)/$', views.quiz, name='quiz'),
    url(r'^end/$', views.end, name='end'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^report/(?P<staff_id>\d+)/$', views.report, name='report'),
)
