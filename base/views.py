from django.contrib.auth import logout as do_logout
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def logout(request):
    return do_logout(request)
