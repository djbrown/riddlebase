from django.contrib import admin

from riddles.models import RiddleState, RiddleType

admin.site.register(RiddleType)
admin.site.register(RiddleState)
