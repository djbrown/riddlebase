import datetime

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import RiddleCategory


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'riddles/index.html')


def category(request: HttpRequest, id: int) -> HttpResponse:
    cat = RiddleCategory.objects.get(id=id)
    return render(request, 'riddles/category.html', {
        "category": cat
    })
