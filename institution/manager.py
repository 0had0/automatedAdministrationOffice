from django.db import models


class InstitutionManager(models.Manager):

    def create_institution(self, name, **extra_fields):
        if not name:
            raise ValueError('The name must be set')
        institution = self.model(name=name, **extra_fields)
        institution.save()
        return institution
