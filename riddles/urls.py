from django.conf.urls import url, include

import sudoku.urls
from . import views

app_name = 'riddles'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sudoku/',  include(sudoku.urls, namespace="sudoku")),
]
