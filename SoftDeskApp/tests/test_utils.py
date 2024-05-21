from django.test import TestCase
from freezegun import freeze_time

from SoftDeskSupport.utils import get_user_age


class TestAge(TestCase):

    @freeze_time("2024-05-09")
    def test_get_user_age(self):
        age = get_user_age("2016-05-09")

        self.assertEqual(age, 8)
