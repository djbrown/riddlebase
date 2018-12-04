import math

from django.core.validators import MinValueValidator
from django.db import models

from riddles.models import Riddle


class Sudoku(models.Model):
    riddle = models.OneToOneField(Riddle, on_delete=models.CASCADE)
    box_rows = models.IntegerField(verbose_name='Number of horizontal box-rows', validators=[
        MinValueValidator(2)])

    @property
    def cells(self) -> int:
        return len(self.riddle.solution)

    @property
    def size(self) -> int:
        return int(math.sqrt(self.cells))

    @property
    def solution_as_list(self) -> list:
        return list(self.riddle.solution)

    @property
    def pattern_as_list(self) -> list:
        return list(self.riddle.pattern)

    @property
    def solution_as_two_dimensional_array(self) -> list:
        array = []
        for row_i in range(self.size):
            cell_i = row_i * self.size
            row = list(self.riddle.solution[cell_i:cell_i + self.size])
            array.append(row)
        return array

    @staticmethod
    def check_solution(pattern, solution) -> bool:
        raise NotImplementedError

    def __str__(self) -> str:
        return "Sudoku: {}".format(self.pk)
