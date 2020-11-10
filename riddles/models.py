from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from riddles import util


class RiddleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField()

    def clean(self):
        if self.parent == self:
            raise ValidationError('You cannot set the parent to the object itself.')

    def __str__(self):
        return "RiddleCategory: {}".format(self.name)


class RiddleType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(RiddleCategory, on_delete=models.CASCADE)

    def __str__(self):
        return "RiddleType: {}".format(self.name)


class Riddle(models.Model):
    riddle_type = models.ForeignKey(RiddleType, on_delete=models.CASCADE)
    solution = models.TextField()
    pattern = models.TextField()
    difficulty = models.PositiveSmallIntegerField(blank=True, null=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(10)])
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    # Todo: add field "created:Time" and "creator:User"
    # Todo: store local copy of included frameworks: bootstrap and jquery

    def previous_pk(self):
        previous_set = Riddle.objects.filter(pk__lt=self.pk).order_by('-pk')
        return previous_set[0].pk if previous_set else None

    def next_pk(self):
        next_set = Riddle.objects.filter(pk__gt=self.pk).order_by('pk')
        return next_set[0].pk if next_set else None

    def clean(self):
        pat_len = len(self.pattern)
        sol_len = len(self.solution)
        if pat_len != sol_len:
            raise ValidationError('Pattern length does not match solution length.')
        if not util.is_square(pat_len):
            raise ValidationError('Riddle value length is not square.')

    def get_or_create_state(self, user: User) -> str:
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

    def get_context(self, user: User) -> dict:
        return {
            "riddle_id": self.pk,
            "riddle_type": self.riddle_type.name,
            "pattern": self.pattern,
            "state": self.get_or_create_state(user),
            'previous_id': self.previous_pk(),
            'next_id': self.next_pk(),
        }

    def __str__(self):
        return "Riddle: {} {}".format(self.riddle_type.name, self.pk)


class RiddleState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    riddle = models.ForeignKey(Riddle, on_delete=models.CASCADE)
    value = models.TextField()
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "riddle")

    def __str__(self) -> str:
        return "RiddleState: {} {}".format(self.riddle, self.user)
