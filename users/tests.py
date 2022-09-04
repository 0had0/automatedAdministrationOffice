from django.test import TestCase

from institution.models import Institution
from users.models import Director


class DirectorTestCase(TestCase):

    DIRECTOR_TEST_DATA = {
        "email": 'test@te.st',
        "first_name": "foo",
        "last_name": "bar",
        "phone_number": 12345678,
        "password": "Test@123"
    }

    def setUp(self):
        inst = Institution.objects.create_institution(name='TEST_NAME')
        Director.objects.create_user(**self.DIRECTOR_TEST_DATA, institution_id=inst.institution_id)

    def test_user_created_success(self):
        inst = Institution.objects.get(name__exact="TEST_NAME")
        director = Director.objects.get(email__exact=self.DIRECTOR_TEST_DATA.get("email"))
        assert director.institution_id == inst.institution_id
        assert director.email == self.DIRECTOR_TEST_DATA.get("email")
        assert director.phone_number == self.DIRECTOR_TEST_DATA.get("phone_number")
        assert director.first_name == self.DIRECTOR_TEST_DATA.get("first_name")
        assert director.last_name == self.DIRECTOR_TEST_DATA.get("last_name")
        assert director.is_director

