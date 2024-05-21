from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from SoftDeskApp.models import Comment, Contributor, Issue, Project
from SoftDeskApp.permissions import (CanManageProjectContributors,
                                     IsOwnerOrReadOnly,
                                     IsProjectContributorAuthenticated,
                                     IsRightUser, SignupViewPermissions)
from SoftDeskApp.serializers import (CommentDetailSerializer,
                                     CommentListSerializer,
                                     ContributorDetailSerializer,
                                     ContributorSerializer,
                                     IssueDetailSerializer,
                                     IssueListSerializer,
                                     ProjectDetailSerializer,
                                     ProjectListSerializer,
                                     UserDetailSerializer, UserListSerializer)
from SoftDeskSupport.utils import get_user_age


class DetailOrListSerializerMixin:
    """
    A mixin that allows multiple serializers to be used, based on the action
    being performed.
    For example, a detailed serializer might be used for the 'retrieve' action,
    while a less detailed serializer might be used for 'list' or 'create'.
    """
    detail_serializer_class = None

    def get_serializer_class(self):
        """
        Return the serializer class to be used for the current action.
        If the current action is 'retrieve', it returns
        'detail_serializer_class'. Otherwise, it calls and returns the
        serializer class from the superclass.
        """
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(DetailOrListSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(contributors=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, contributors=[self.request.user])


class IssueViewSet(DetailOrListSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsOwnerOrReadOnly, IsProjectContributorAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get("project")
        if project_id:
            return Issue.objects.filter(project_id=project_id)
        return Issue.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(DetailOrListSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserListViewSet(DetailOrListSerializerMixin, ModelViewSet):

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    permission_classes = [IsRightUser]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        password = self.request.data["password"]
        hashed_password = make_password(password)

        serializer.save(
            age=get_user_age(self.request.data["birth_date"]),
            password=hashed_password
        )


class SignUpUserViewSet(ModelViewSet):

    serializer_class = UserDetailSerializer
    permission_classes = [SignupViewPermissions]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        password = self.request.data.get("password")
        birth_date = self.request.data.get("birth_date")
        hashed_password = make_password(password)

        serializer.save(
            age=get_user_age(birth_date),
            password=hashed_password
        )


class ContributorViewSet(DetailOrListSerializerMixin, ModelViewSet):

    serializer_class = ContributorSerializer
    detail_serializer_class = ContributorDetailSerializer
    permission_classes = [CanManageProjectContributors, IsProjectContributorAuthenticated]

    def get_queryset(self):
        return Contributor.objects.all()
