import datetime

from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from RiddleBase import settings
from .models import *


def index(request):
    return render(request, 'riddles/index.html')


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        days_expire = 365

    max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
    response.set_cookie(key, value, max_age=max_age, expires=expires,
                        domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)
