from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from riddles.models import Riddle
from sudoku.models import Sudoku


def view_index(request) -> HttpResponse:
    return render(request, 'sudoku/index.html', {
        'pks': list(sudoku.pk for sudoku in Riddle.objects.filter(riddle_type__name='sudoku')),
    })


def view_riddle(request: HttpRequest, sudoku_number: int) -> HttpResponse:
    try:
        riddle = Riddle.objects.get(pk=riddle_id)
        sudoku = Sudoku(riddle)
    except Sudoku.DoesNotExist:
        raise Http404("Sudoku does not exist")

    context = sudoku.get_context(request.user)
    context.update({
        'box_rows': sudoku.box_rows,
    })
    return render(request, 'sudoku/riddle.html', context)


def view_creator(request: HttpRequest) -> HttpResponse:
    return render(request, 'sudoku/creator.html')


@csrf_exempt
@require_POST
def rest_check(request: HttpRequest, riddle_id: int) -> JsonResponse:
    try:
        sudoku = Sudoku.objects.get(pk=riddle_id)
    except Sudoku.DoesNotExist:
        raise Http404("Sudoku does not exist")

    proposal = request.POST.get("proposal")
    correct = proposal is not None and proposal == sudoku.solution
    response = {'correct': correct}
    return JsonResponse(response)


@require_POST
def rest_create(request: HttpRequest) -> JsonResponse:
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
    return JsonResponse({'pk': created.pk})
