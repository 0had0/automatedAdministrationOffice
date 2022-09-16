import os
import django

from institution.models import Institution
from auth.models import Account

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "automatedAdministrationOffice.settings")

django.setup()


institution = Institution.objects.create_institution(
    name="Super User Institution",
    email="super@user.com",
    phone_number=00000000
)

Account.objects.create_superuser(
    first_name="Hadi",
    last_name="Houssainy",
    email="hh@admin.com",
    password="password1",
    institution_id=institution.institution_id
)
