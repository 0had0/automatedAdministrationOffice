from django.db import models

from auth.models import Account
from institution.models import Institution

from .managers import (DirectorManager, UserManager, ReviewerManager)


class Director(Account):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    objects = DirectorManager()

    def __str__(self):
        return "< Director: {} >".format(Account.__str__(self))

    class Meta:
        db_table = 'directors'


class User(Account):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    objects = UserManager()


class Reviewer(Account):
    # TODO: add reviewer permissions, aka. difference between this class and User class
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    objects = ReviewerManager()
