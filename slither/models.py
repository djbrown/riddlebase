from django.contrib.auth.models import User
from django.db import models

from riddles.models import RiddleType, Riddle


class Slither(Riddle):
    breadth = models.IntegerField()

    @staticmethod
    def check_solution(pattern: str, solution: str) -> bool:
        pass
