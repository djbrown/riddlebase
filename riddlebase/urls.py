from django.contrib import admin
from django.urls import include, path

import riddles.urls
from base.views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('riddles/', include(riddles.urls)),
]
