from django.urls import include, path


from . import views

app_name = 'riddles'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>/', views.category, name='category'),
    path('type/<int:pk>/', views.riddle_type, name='type'),
    path('riddle/<int:pk>/', views.riddle, name='riddle'),
]
