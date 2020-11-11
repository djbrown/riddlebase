import datetime

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Riddle, RiddleCategory, RiddleType


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'riddles/index.html')


def category(request: HttpRequest, id: int) -> HttpResponse:
    riddle_category = RiddleCategory.objects.get(id=id)
    return render(request, 'riddles/category.html', {
        "category": riddle_category,
    })


def riddle_type(request: HttpRequest, id: int) -> HttpResponse:
    _riddle_type = RiddleType.objects.get(id=id)
    return render(request, 'riddles/type.html', {
        "riddle_type": _riddle_type,
    })


def riddle(request: HttpRequest, id: int) -> HttpResponse:
    riddle = Riddle.objects.get(id=id)
    context = {
        'riddle': riddle,
    }

    state = request.POST.get('state', request.session.get('state', riddle.pattern))
    if request.POST.get('revert'):
        state = riddle.pattern
    request.session['state'] = state
    context['state'] = state

    if state == riddle.solution:
        context['correct'] = True

    if request.POST.get('check'):
        if state != riddle.solution:
            context['incorrect'] = True

    return render(request, 'riddles/riddle.html', context)
