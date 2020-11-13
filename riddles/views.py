import datetime

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
        'previous': Riddle.objects.filter(pk__lt=pk).order_by('pk').last(),
        'next': Riddle.objects.filter(pk__gt=pk).order_by('pk').first(),
    }

    state = request.POST.get('state', request.session.get('state', riddle.pattern))
    if request.POST.get('revert'):
        state = riddle.pattern
    request.session['state'] = state
    context['state'] = state

    if state == riddle.solution:
        context['correct'] = True

    if request.POST.get('submit'):
        if state != riddle.solution:
            context['incorrect'] = True

    return render(request, 'riddles/riddle.html', context)


@csrf_exempt
@require_POST
def check(request: HttpRequest, pk: int) -> JsonResponse:
    riddle = get_object_or_404(Riddle, pk=pk)

    state = request.POST.get("state")
    correct = state == riddle.solution
    response = {'correct': correct}
    return JsonResponse(response)
