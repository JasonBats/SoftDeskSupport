from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse_lazy
from rest_framework import status

from SoftDeskApp.models import Project


class PermissionsTests(APITestCase):
    def setUp(self):

        self.client = APIClient()

        self.staff_user = get_user_model().objects.create(
            username='staff_user',
            birth_date='1990-09-09',
            age=50,
            is_superuser=False,
            is_staff=True,
        )

        self.employee_user = get_user_model().objects.create(
            username='employee_user',
            birth_date='1990-09-09',
            age=50,
            is_superuser=False,
            is_staff=False,
        )

        self.second_employee_user = get_user_model().objects.create(
            username='second_employee_user',
            birth_date='1990-09-09',
            age=50,
            is_superuser=False,
            is_staff=False,
        )

        self.project = Project.objects.create(
            name='API_TEST_PROJECT_MODEL',
            description='API_TEST_PROJECT_DESCRIPTION',
            type='iOS',
            author=self.staff_user,
        )

    def test_patch_project_without_permission(self):
        self.client.force_authenticate(user=self.employee_user)

        url = reverse_lazy('project-detail', kwargs={'pk': 1})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_project_with_permission(self):
        self.client.force_authenticate(user=self.staff_user)

        url = reverse_lazy('project-detail', kwargs={'pk': 1})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_info_with_permission(self):
        self.client.force_authenticate(user=self.employee_user)

        url = reverse_lazy('user-detail', kwargs={'pk': self.employee_user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_info_without_permission(self):
        self.client.force_authenticate(user=self.second_employee_user)

        url = reverse_lazy('user-detail', kwargs={'pk': self.employee_user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_info_as_staff(self):
        self.client.force_authenticate(user=self.staff_user)

        url = reverse_lazy('user-detail', kwargs={'pk': self.employee_user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
