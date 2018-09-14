from django.shortcuts import render

from riddles.models import RiddleCategory


def index(request):
    context = {
        'category_list': RiddleCategory.objects.all()
    }
    return render(request, 'index.html', context)
