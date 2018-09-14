from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from slither.models import Slither


def view_index(request):
    return render(request, 'slither/index.html', {
        'pks': list(riddle.pk for riddle in Slither.objects.all()),
    })


def view_riddle(request, riddle_id):
    try:
        riddle = Slither.objects.get(pk=riddle_id)
    except Slither.DoesNotExist:
        raise Http404("Riddle does not exist")

    context = riddle.get_context(request.user)
    context.update({"breadth": riddle.breadth})
    return render(request, 'slither/riddle.html', context)


@csrf_exempt
@require_POST
def rest_check(request, riddle_id):
    try:
        riddle = Slither.objects.get(pk=riddle_id)
    except Slither.DoesNotExist:
        raise Http404("Riddle does not exist")

    proposal = request.POST.get("proposal")
    correct = proposal is not None and proposal == riddle.solution
    response = {'correct': correct}
    return JsonResponse(response)


def view_creator(request):
    return render(request, 'slither/creator.html')


@require_POST
def rest_create(request: HttpRequest) -> JsonResponse:
    error = []
    if not request.user.has_perm("riddles.add_slither"):
        error.append("no permission")

    solution = request.POST.get("slither")
    pattern = request.POST.get("pattern")

    if solution is None:
        error.append("no solution")
    if pattern is None:
        error.append("no pattern")

    if error:
        return JsonResponse({'error': error})

    created = Slither(solution=solution,
                      pattern=pattern,
                      state=pattern,
                      difficulty=5,
                      box_rows=3)
    created.save()
    return JsonResponse({'id': created.id})
