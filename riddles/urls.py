from django.urls import include, path

import slither.urls
import sudoku.urls

from . import views

app_name = 'riddles'

urlpatterns = [
    path('', views.index, name='index'),
    path('slither/', include(slither.urls)),
    path('sudoku/', include(sudoku.urls)),
]
