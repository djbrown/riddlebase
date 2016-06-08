from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from riddles.models import Sudoku, RiddleState
from slither.models import Slither


def view_index(request):
    return render(request, 'slither/index.html', {
        'ids': list(slither.id for slither in Slither.objects.all()),
    })


def view_riddle(request, riddle_id):
    try:
        slither = Slither.objects.get(pk=riddle_id)
    except Slither.DoesNotExist:
        raise Http404("Sudoku does not exist")

    return render(request, 'sudoku/riddle.html', slither.get_context(request.user))


@csrf_exempt
@require_POST
def rest_check(request, riddle_id):
    try:
        riddle = Sudoku.objects.get(pk=riddle_id)
    except Sudoku.DoesNotExist:
        raise Http404("Sudoku does not exist")

    proposal = request.POST.get("proposal")
    correct = proposal is not None and proposal == riddle.solution
    response = {'correct': correct}
    return JsonResponse(response)


def view_creator(request):
    return render(request, 'sudoku/creator.html')


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
    return JsonResponse({'id': created.id})
