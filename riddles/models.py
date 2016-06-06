from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from riddles import util


class RiddleType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "RiddleType: {}".format(self.name)


class Riddle(models.Model):
    riddle_type = models.ForeignKey(RiddleType)
    solution = models.TextField()
    pattern = models.TextField()
    difficulty = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)])
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    # Todo: add field "created:Time" and "creator:User"
    # Todo: store local copy of included frameworks: bootstrap and jquery

    def previous_id(self):
        previous_set = Riddle.objects.filter(id__lt=self.id).order_by('-id')
        return previous_set[0].id if previous_set else None

    def next_id(self):
        next_set = Riddle.objects.filter(id__gt=self.id).order_by('id')
        return next_set[0].id if next_set else None

    def clean(self):
        pat_len = len(self.pattern)
        sol_len = len(self.solution)
        if pat_len != sol_len:
            raise ValidationError('Pattern length does not match solution length.')
        if not util.is_square(pat_len):
            raise ValidationError('Riddle value length is not square.')

    @staticmethod
    def check_solution(pattern, solution) -> bool:
        raise NotImplementedError()

    def get_or_create_state(self, user):
        state_values = self.pattern
        if user.is_authenticated():
            try:
                state = self.riddlestate
                state_values = state.values
            except ObjectDoesNotExist:
                state = RiddleState(user=user, riddle=self, values=self.pattern)
                state.save()
                state_values = state.values
        return state_values

    def get_context(self, user) -> dict:
        return {
            "riddle_id": self.id,
            "riddle_type": self.riddle_type.name,
            "pattern": self.pattern,
            "state": self.get_or_create_state(user),
            'previous_id': self.previous_id(),
            'next_id': self.next_id(),
        }

    def __str__(self):
        return "Riddle: {} {}".format(self.riddle_type.name, self.id)


class RiddleState(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    riddle = models.OneToOneField(Riddle, models.CASCADE)
    grid = models.TextField()
    values = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    finished = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "riddle")

    def __str__(self) -> str:
        return "RiddleState-{}-{}".format(self.riddle, self.user)


def instances(model: models.Model) -> list:
    instance_list = []
    if not model._meta.abstract:
        instance_list.extend(model.objects.all())
    for sub_model in model.__subclasses__():
        instance_list.extend(instances(sub_model))
    return instance_list
