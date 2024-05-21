from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from SoftDeskApp.models import Contributor, Project


class PermissionsTests(APITestCase):
    def setUp(self):

        self.client = APIClient()

        self.staff_user = get_user_model().objects.create(
            username="staff_user",
            birth_date="1990-09-09",
            age=50,
            is_superuser=False,
            is_staff=True,
        )

        self.employee_user = get_user_model().objects.create(
            username="employee_user",
            birth_date="1990-09-09",
            age=50,
            is_superuser=False,
            is_staff=False,
        )

        self.second_employee_user = get_user_model().objects.create(
            username="second_employee_user",
            birth_date="1990-09-09",
            age=50,
            is_superuser=False,
            is_staff=False,
        )

        self.project = Project.objects.create(
            name="API_TEST_PROJECT_MODEL",
            description="API_TEST_PROJECT_DESCRIPTION",
            type="iOS",
            author=self.staff_user,
        )

        self.contributors = Contributor.objects.create(
            user=self.staff_user, project=self.project
        )

        self.contributors = Contributor.objects.create(
            user=self.second_employee_user, project=self.project
        )

    def test_get_project_IsProjectContributorAuthenticated_True(self):
        self.client.force_authenticate(user=self.staff_user)

        url = reverse_lazy("project-detail", kwargs={"pk": self.project.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project_IsProjectContributorAuthenticated_False(self):
        self.client.force_authenticate(user=self.employee_user)

        url = reverse_lazy("project-detail", kwargs={"pk": self.project.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_new_project(self):
        self.client.force_authenticate(user=self.second_employee_user)

        url = reverse_lazy("project-list")
        data = {
            "name": "Projet TEST auteur = contributeur",
            "description": "Test permissions",
            "author": self.second_employee_user.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_issue_IsProjectContributorAuthenticated_True(self):
        self.client.force_authenticate(user=self.second_employee_user)

        url = reverse_lazy("issue-list")
        data = {
            "name": "Issue 2 projet 17",
            "description": "Description de l'issue",
            "project": self.project.id,
            "priority": "HIGH",
            "nature": "BUG",
            "status": "Finished",
            "author": self.second_employee_user.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_issue_IsProjectContributorAuthenticated_False(self):
        self.client.force_authenticate(user=self.employee_user)

        url = reverse_lazy("issue-list")
        data = {
            "name": "Issue 1 projet 1",
            "description": "Description de l'issue",
            "project": self.project.id,
            "priority": "HIGH",
            "nature": "BUG",
            "status": "Finished",
            "author": self.employee_user.id,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_project_issues_IsProjectContributorAuthenticated_True(self):
        self.client.force_authenticate(user=self.employee_user)

        url = reverse_lazy("issue-list")
        query_params = {"project": self.project.id}
        full_url = f"{url}?{urlencode(query_params)}"
        response = self.client.get(full_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_project_IsOwnerOrReadOnly_True(self):
        self.client.force_authenticate(user=self.staff_user)

        url = reverse_lazy("project-detail", kwargs={"pk": 1})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_details_IsRightUser_True(self):
        self.client.force_authenticate(user=self.employee_user)

        url = reverse_lazy("user-detail", kwargs={"pk": self.employee_user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_details_IsRightUser_False(self):
        self.client.force_authenticate(user=self.second_employee_user)

        url = reverse_lazy("user-detail", kwargs={"pk": self.employee_user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_details_IsRightUser_True_staff(self):
        self.client.force_authenticate(user=self.staff_user)

        url = reverse_lazy("user-detail", kwargs={"pk": self.employee_user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_manage_project_contributors_IsProjectContributor_False(self):
        self.client.force_authenticate(user=self.employee_user)

        url = reverse_lazy("contributor-detail", kwargs={"pk": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_manage_project_contributors_IsProjectContributor_True(self):
        self.client.force_authenticate(user=self.staff_user)

        url = reverse_lazy("contributor-detail", kwargs={"pk": 1})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_get_project_contributors_IsProjectContributor_False(self):
        self.client.force_authenticate(user=self.employee_user)

        url = reverse_lazy("contributor-detail", kwargs={"pk": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_get_project_contributors_IsProjectContributor_True(self):
        self.client.force_authenticate(user=self.staff_user)

        url = reverse_lazy("contributor-detail", kwargs={"pk": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_signup_too_young(self):
        url = reverse_lazy("signup-list")
        data = {
            "password": "testmdp",
            "username": "TestUser3",
            "birth_date": "2016-09-09",
            "can_be_contacted": True,
            "can_be_shared": False,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_signup(self):
        url = reverse_lazy("signup-list")
        data = {
            "password": "testmdp",
            "username": "TestUser3",
            "birth_date": "1990-09-09",
            "can_be_contacted": True,
            "can_be_shared": False,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["age"], 33)

    def test_can_create_a_user(self):
        url = reverse_lazy("user-list")
        data = {
            "password": "abcd123",
            "is_superuser": False,
            "username": "NouvelEmployé",
            "first_name": "",
            "last_name": "",
            "email": "test@test.test",
            "is_staff": False,
            "is_active": True,
            "birth_date": "1990-09-09",
            "age": 0,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["age"], 33)

    def test_create_comment_IsProjectContributor_True(self):
        self.client.force_authenticate(user=self.second_employee_user)
        url_issue = reverse_lazy("issue-list")
        data_issue = {
            "name": "Issue 1 projet 1",
            "description": "Description de l'issue",
            "project": self.project.id,
            "priority": "HIGH",
            "nature": "BUG",
            "status": "Finished",
            "author": self.second_employee_user.id,
        }
        self.client.post(url_issue, data_issue, format="json")
        url = reverse_lazy("comment-list")
        data = {
            "issue": 1,
            "description": "Commentaire à propos de l'issue 1 du projet 1",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
