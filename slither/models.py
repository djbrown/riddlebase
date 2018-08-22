from django.db import models

from riddles.models import Riddle


class Slither(Riddle):
    width = models.IntegerField()
    height = models.IntegerField()

    @staticmethod
    def check_solution(pattern: str, solution: str) -> bool:
        pass


class Square(Slither):
    pass
