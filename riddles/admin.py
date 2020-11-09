from django.contrib import admin

from riddles.models import Riddle, RiddleCategory, RiddleState, RiddleType

admin.site.register(RiddleCategory)
admin.site.register(RiddleType)
admin.site.register(Riddle)
admin.site.register(RiddleState)
