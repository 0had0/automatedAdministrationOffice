from django.db import models

from institution.models import Institution


class MyAccountManager(models.Manager):

    def get_by_natural_key(self, username):
        return self.get(email=username)

    def create_user(self, email, password, first_name, last_name, institution, **kwargs):
        if not email:
            raise ValueError('Users must have a Email')

        if not first_name or not last_name:
            raise ValueError('User must have a name')

        if not institution:
            return ValueError("Institution id is required")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            institution=Institution.objects.get(pk=institution),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name, **kwargs):
        if not email:
            raise ValueError('Users must have a Email')

        if not first_name or not last_name:
            raise ValueError('User must have a name')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=True,
            is_superuser=True,
            is_director=True,
            is_reviewer=True,
            is_admin=True,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
