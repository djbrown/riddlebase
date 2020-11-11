import datetime

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Riddle, RiddleCategory, RiddleType


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'riddles/index.html')


def category(request: HttpRequest, pk: int) -> HttpResponse:
    riddle_category = get_object_or_404(RiddleCategory, pk=pk)
    return render(request, 'riddles/category.html', {
        "category": riddle_category,
    })


def riddle_type(request: HttpRequest, pk: int) -> HttpResponse:
    _riddle_type = get_object_or_404(RiddleType, pk=pk)
    return render(request, 'riddles/type.html', {
        "riddle_type": _riddle_type,
    })


def riddle(request: HttpRequest, pk: int) -> HttpResponse:
    riddle = get_object_or_404(Riddle, pk=pk)
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
