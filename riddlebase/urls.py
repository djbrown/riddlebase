from django.contrib.auth import urls as auth_urls
from django.urls import include, path

import base.views
import riddles.urls

urlpatterns = [
    path('', base.views.index, name='index'),
    path('riddles/', include(riddles.urls)),
    path('accounts/', include(auth_urls)),
]
