from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse_lazy
from rest_framework import status


class PermissionsTests(APITestCase):
    def setUp(self):

        self.client = APIClient()

        self.admin_user = get_user_model().objects.create(
                    username='admin_user',
                    birth_date='1990-09-09',
                    age=50,
                    is_superuser=True,
                    is_staff=False,
                )

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

    def test_admin_restricted_view_without_permission(self):
        """
        View requires authenticated-superuser permission.
        User only has staff permission.
        403 is expected.
        """
        self.client.force_authenticate(user=self.staff_user)

        url = reverse_lazy('admin-project-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_restricted_view_without_authentication(self):
        """
        View requires authenticated-superuser permission.
        Client is anonymous.
        401 is expected.
        """
        url = reverse_lazy('admin-project-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_restricted_view_with_permission(self):
        """
        View requires authenticated-superuser permission.
        User is superuser
        200 is expected.
        """
        self.client.force_authenticate(user=self.admin_user)

        url = reverse_lazy('admin-project-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_restricted_view_without_permission(self):
        self.client.force_authenticate(user=self.employee_user)

        url = reverse_lazy('staff-issue-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_restricted_view_with_permission(self):
        self.client.force_authenticate(user=self.staff_user)

        url = reverse_lazy('staff-issue-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_restricted_view_without_authentication(self):
        url = reverse_lazy('staff-issue-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

