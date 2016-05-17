import datetime

from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from RiddleBase import settings
from .models import *


def index(request):
    return render(request, 'riddles/index.html')


def sudokus(request):
    return render(request, 'riddles/sudokus.html', {
        'ids': list(riddle.id for riddle in Sudoku.objects.all()),
    })


def sudoku(request, riddle_id):
    try:
        riddle = Sudoku.objects.get(pk=riddle_id)
    except Sudoku.DoesNotExist:
        raise Http404("Sudoku does not exist")

    state_value = riddle.pattern
    if request.user.is_authenticated():
        states = RiddleState.objects.filter(user=request.user, riddle=riddle)
        if len(states) is 1:
            state_value = states[0].value
        elif len(states) is 0:
            state = RiddleState(user=request.user, riddle=riddle, value=riddle.pattern)
            state.save()
            state_value = state.value

    return render(request, 'riddles/sudoku.html', {
        'riddle_type': 'Riddle',
        'riddle_id': riddle.id,
        'pattern': riddle.pattern,
        'state': state_value,
        'box_rows': riddle.box_rows,
        'previous_id': riddle.previous_id(),
        'next_id': riddle.next_id(),
    })


@csrf_exempt
@require_POST
def sudoku_check(request, riddle_id):
    try:
        riddle = Sudoku.objects.get(pk=riddle_id)
    except Sudoku.DoesNotExist:
        raise Http404("Sudoku does not exist")

    proposal = request.POST.get("proposal")
    correct = proposal is not None and proposal == riddle.solution
    response = {'correct': correct}
    return JsonResponse(response)


def sudoku_creator(request):
    return render(request, 'riddles/sudoku-creator.html')


@require_POST
def create_sudoku(request):
    error = []
    if not request.user.has_perm("riddles.add_sudoku"):
        error.append("no permission")

    solution = request.POST.get("solution")
    pattern = request.POST.get("pattern")

    if solution is None:
        error.append("no solution")
    if pattern is None:
        error.append("no pattern")

    if error:
        return JsonResponse({'error': error})

    created = Sudoku(solution=solution,
                     pattern=pattern,
                     state=pattern,
                     difficulty=5,
                     box_rows=3)
    created.save()
    return JsonResponse({'id': created.id})


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        days_expire = 365

    max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
    response.set_cookie(key, value, max_age=max_age, expires=expires,
                        domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)
