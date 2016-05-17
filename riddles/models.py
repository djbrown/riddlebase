import math

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class RiddleType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def __str__(self):
        return "RiddleType: {}".format(self.name)


class Riddle(models.Model):
    type = models.ForeignKey(RiddleType)
    solution = models.TextField()
    pattern = models.TextField()
    difficulty = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)])
    objects = models.Manager()

    def previous_id(self):
        previous_set = Sudoku.objects.filter(id__lt=self.id).order_by('id')
        return previous_set.get().id if previous_set else None

    def next_id(self):
        next_set = Sudoku.objects.filter(id__gt=self.id).order_by('-id')
        return next_set.get().id if next_set else None

    class Meta:
        abstract = True


class Sudoku(Riddle):
    # TODO assign Sudoku-RiddleType instance to this type
    box_rows = models.IntegerField(verbose_name='Number of horizontal box-rows', validators=[
        MinValueValidator(2)])

    @property
    def cells(self) -> int:
        return len(self.solution)

    @property
    def size(self) -> int:
        return int(math.sqrt(self.cells))

    @property
    def solution_as_list(self) -> list:
        return list(self.solution)

    @property
    def pattern_as_list(self) -> list:
        return list(self.pattern)

    @property
    def solution_as_two_dimensional_array(self) -> list:
        array = []
        for row_i in range(self.size):
            cell_i = row_i * self.size
            row = list(self.solution[cell_i:cell_i + self.size])
            array.append(row)
        return array

    @property
    def state_as_two_dimensional_array(self) -> list:
        array = []
        for row_i in range(self.size):
            cell_i = row_i * self.size
            row = list(self.state[cell_i:cell_i + self.size])
            array.append(row)
        return array

    @property
    def box_columns(self) -> int:
        return int(self.size / self.box_rows)

    def __str__(self) -> str:
        return "Sudoku-{}".format(self.id)


class RiddleState(models.Model):
    user = models.ForeignKey(User, models.CASCADE)  # editable=False)
    riddle = models.ForeignKey(Sudoku, models.CASCADE)  # editable=False)
    value = models.TextField()

    class Meta:
        unique_together = ("user", "riddle")

    @property
    def finished(self) -> bool:
        return self.state == self.riddle.solution

    def __str__(self) -> str:
        return "RiddleState-{}-{}".format(self.riddle, self.user)


def instances(model: models.Model) -> list:
    instance_list = []
    if not model._meta.abstract:
        instance_list.extend(model.objects.all())
    for sub_model in model.__subclasses__():
        instance_list.extend(instances(sub_model))
    return instance_list
