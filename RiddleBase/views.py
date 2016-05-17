from django.shortcuts import render
from django.contrib.auth.views import \
    login as do_login,\
    logout as do_logout


def index(request):
    return render(request, 'index.html')


def login(request):
    return do_login(request)


def logout(request):
    return do_logout(request)
