from django.conf.urls import url

from . import views

app_name = 'slither'

urlpatterns = [
    url(r'^$', views.view_index, name='index'),
    url(r'^(?P<riddle_id>[0-9]+)/$', views.view_riddle, name='riddle'),
    url(r'^create/$', views.view_creator, name='creator'),
    url(r'^(?P<riddle_id>[0-9]+)/check/$', views.rest_check, name='check'),
    url(r'^submit-new/$', views.rest_create, name='create'),
]
