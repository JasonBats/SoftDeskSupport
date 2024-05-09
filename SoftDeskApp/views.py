from django.contrib.auth.hashers import make_password

from SoftDeskApp.models import Project, Issue, Comment, Contributor
from SoftDeskSupport.utils import get_user_age
from authentication.models import User

from SoftDeskApp.serializers import (ProjectListSerializer,
                                     ProjectDetailSerializer,
                                     IssueListSerializer,
                                     IssueDetailSerializer,
                                     CommentListSerializer,
                                     CommentDetailSerializer,
                                     UserListSerializer,
                                     UserDetailSerializer,
                                     ContributorSerializer,
                                     ContributorDetailSerializer)

from rest_framework.viewsets import ModelViewSet
from SoftDeskApp.permissions import (IsProjectContributorAuthenticated,
                                     IsRightUser,
                                     IsOwnerOrReadOnly,
                                     CanManageProjectContributors,
                                     SignupViewPermissions)


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsOwnerOrReadOnly, IsProjectContributorAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, contributors=[self.request.user])


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsOwnerOrReadOnly, IsProjectContributorAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return Issue.objects.filter(project_id=project_id)
        return Issue.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly, IsProjectContributorAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserListViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    permission_classes = [IsRightUser]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        password = self.request.data['password']
        hashed_password = make_password(password)
        serializer.save(
            age=get_user_age(self.request.data['birth_date']),
            password=hashed_password
        )


class SignUpUserViewSet(ModelViewSet):

    serializer_class = UserDetailSerializer
    permission_classes = [SignupViewPermissions]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        password = self.request.data['password']
        hashed_password = make_password(password)
        serializer.save(
            age=get_user_age(self.request.data['birth_date']),
            password=hashed_password
        )


class ContributorViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorSerializer
    detail_serializer_class = ContributorDetailSerializer
    permission_classes = [CanManageProjectContributors]

    def get_queryset(self):
        return Contributor.objects.all()
