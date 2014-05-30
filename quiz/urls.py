from django.conf.urls import patterns, url

from quiz import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^t/(?P<staff_id>\d+)/$', views.quiz, name='quiz'),
)
