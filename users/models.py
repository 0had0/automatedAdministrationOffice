from django.db import models

from auth.models import Account
from institution.models import Institution

from .managers import (DirectorManager, UserManager, ReviewerManager)


class Director(Account):
    objects = DirectorManager()

    def __str__(self):
        return "< Director: {} >".format(Account.__str__(self))

    class Meta:
        db_table = 'directors'


class User(Account):
    objects = UserManager()

    class Meta:
        db_table = 'users'


class Reviewer(Account):
    objects = ReviewerManager()

    class Meta:
        db_table = 'reviewers'
