from django.urls import include, path

# import slither.urls
# import sudoku.urls

from . import views

app_name = 'riddles'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:id>/', views.category, name='category'),
    path('type/<int:id>/', views.riddle_type, name='riddle-type'),
    path('riddle/<int:id>/', views.riddle, name='riddle'),
    # path('slither/', include(slither.urls)),
    # path('sudoku/', include(sudoku.urls)),
]
