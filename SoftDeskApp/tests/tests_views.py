from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from SoftDeskApp.models import Project, Issue, Comment
from SoftDeskApp.serializers import IssueListSerializer, ProjectListSerializer


class SoftDeskAppAPITestCase(APITestCase):

    def format_datetime(self, date):
        return date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def serialize_issues_list(self, data, is_many):
        issues_list_serializer = IssueListSerializer(data, many=is_many)
        serialized_issues = issues_list_serializer.data
        return serialized_issues

    def serialize_projects_list(self, data, is_many):
        projects_list_serializer = ProjectListSerializer(data, many=is_many)
        serialized_projects = projects_list_serializer.data
        return serialized_projects

    def setUp(self):

        self.client = APIClient()

        self.user_api_test = get_user_model().objects.create(
                    username='test_user_api',
                    birth_date='1990-09-09',
                    age=50,
                )
        self.project = Project.objects.create(
            name='API_TEST_PROJECT_MODEL',
            description='API_TEST_PROJECT_DESCRIPTION',
            type='iOS',
            author=self.user_api_test,
        )

        self.issue = Issue.objects.create(
            name='API_TEST_ISSUE_MODEL',
            description='API_TEST_ISSUE_DESCRIPTION',
            priority='HIGH',
            nature='BUG',
            status='To do',
            assigned_to=self.user_api_test,
            author_id=self.user_api_test.id,
            project_id=self.project.id,
        )

        self.comment = Comment.objects.create(
            description='API_TEST_COMMENT_MODEL_DESCRIPTION',
            issue_id=self.issue.id,
            author_id=self.user_api_test.id,
        )

    def test_project_list(self):

        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                'id': self.project.id,
                'name': self.project.name,
                'description': self.project.description,
                'author': self.project.author_id,
                'number_of_issues':
                    Issue.objects.filter(project=self.project).count(),
            }]
        }

        response = self.client.get(reverse_lazy('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.json())

    def test_project_detail(self):

        expected = {
            'id': self.project.id,
            'issues': self.serialize_issues_list(
                self.project.Issues, True
            ),
            'name': self.project.name,
            'description': self.project.description,
            'type': self.project.type,
            'date_created': self.format_datetime(self.project.date_created),
            'date_updated': self.format_datetime(self.project.date_updated),
            'author': self.project.author_id,
            'contributors': [],
        }

        response = self.client.get(
            reverse_lazy('project-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.json())
        # assert expected == response.json()

    def test_issue_list(self):

        expected = {
            'count': Issue.objects.count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.issue.id,
                    'name': self.issue.name,
                    'description': self.issue.description,
                    'author': self.issue.author_id,
                    'assigned_to': self.issue.assigned_to_id,
                }
            ]
        }

        response = self.client.get(reverse_lazy('issue-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.json())

    def test_issue_detail(self):

        expected = {
            'id': self.issue.id,
            'project':
                self.serialize_projects_list(self.issue.project, False),
            'name': self.issue.name,
            'description': self.issue.description,
            'date_created': self.format_datetime(self.issue.date_created),
            'date_updated': self.format_datetime(self.issue.date_updated),
            'priority': self.issue.priority,
            'nature': self.issue.nature,
            'status': self.issue.status,
            'author': self.issue.author_id,
            'assigned_to': self.issue.assigned_to_id
        }

        response = self.client.get(
            reverse_lazy('issue-detail', kwargs={'pk': self.issue.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.json())

    def test_comment_list(self):

        expected = {
            'count': Comment.objects.count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.comment.id,
                    'issue': self.comment.issue_id
                }
            ]

        }

        response = self.client.get(reverse_lazy('comment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.json())

    def test_comment_detail(self):

        expected = {
            'id': self.comment.id,
            'issue': self.serialize_issues_list(self.comment.issue, False),
            'description': self.comment.description,
            'date_created': self.format_datetime(self.comment.date_created),
            'date_updated': self.format_datetime(self.comment.date_updated),
            'author': self.comment.author_id,
        }

        response = self.client.get(
            reverse_lazy('comment-detail', kwargs={'pk': self.comment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected, response.json())
