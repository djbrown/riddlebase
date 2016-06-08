from django.conf.urls import url

from . import views

app_name = 'riddles'
urlpatterns = [
    url(r'^$', views.view_index, name='index'),
    url(r'^(?P<riddle_id>[0-9]+)/$', views.view_riddle, name='riddle'),
    url(r'^(?P<riddle_id>[0-9]+)/check/$', views.check, name='check'),
    url(r'^create/$', views.creator, name='creator'),
    url(r'^submit-new/$', views.create, name='create'),
]
