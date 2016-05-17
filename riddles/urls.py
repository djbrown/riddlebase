from django.conf.urls import url

from . import views

app_name = 'riddles'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sudoku/$', views.sudokus, name='sudokus'),
    url(r'^sudoku/(?P<riddle_id>[0-9]+)/$', views.sudoku, name='sudoku'),
    url(r'^sudoku/(?P<riddle_id>[0-9]+)/check/$', views.sudoku_check, name='sudoku-check'),
    url(r'^sudoku/create/$', views.sudoku_creator, name='sudoku-creator'),
    url(r'^sudoku/submit-new/$', views.create_sudoku, name='sudoku-create'),
]
