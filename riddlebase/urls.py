from django.contrib import admin
from django.urls import include, path

import riddles.urls
import users.urls
from base.views import index

urlpatterns = [
    path('', index, name='index'),
    path('riddles/', include(riddles.urls)),
    path('users/', include(users.urls)),
    path('admin/', admin.site.urls),
]
