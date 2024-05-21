from rest_framework import serializers

from authentication.models import User
from SoftDeskApp.models import Comment, Contributor, Issue, Project
from SoftDeskSupport.utils import get_user_age


class ProjectDetailSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "issues",
            "name",
            "description",
            "type",
            "date_created",
            "date_updated",
            "author",
            "contributors",
        ]

    def get_issues(self, instance):
        issues_queryset = Issue.objects.filter(project=instance)
        serializer = IssueListSerializer(issues_queryset, many=True)
        return serializer.data


class ProjectListSerializer(serializers.ModelSerializer):

    number_of_issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "author",
            "number_of_issues",
            "contributors",
        ]

    def get_number_of_issues(self, instance):
        number_of_issues_queryset = Issue.objects.filter(
            project=instance
        ).count()
        return number_of_issues_queryset


class IssueDetailSerializer(serializers.ModelSerializer):

    project = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "project",
            "comments",
            "name",
            "description",
            "date_created",
            "date_updated",
            "priority",
            "nature",
            "status",
            "author",
            "assigned_to",
        ]

    def get_project(self, instance):
        queryset = instance.project
        serializer = ProjectListSerializer(queryset, many=False)
        return serializer.data

    def get_comments(self, instance):
        queryset = instance.comments
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "name",
            "description",
            "author",
            "assigned_to",
            "project",
            "priority",
            "nature",
            "status",
        ]

    def validate(self, data):
        project = data.get("project")
        assigned_to = data.get("assigned_to")

        if project and assigned_to:
            contributors = [
                user.user_id for user in Contributor.objects.filter(
                    project=project
                )
            ]
            if assigned_to not in contributors:
                raise serializers.ValidationError(
                    "You can't assign this issue to someone"
                    " not contributing to this project"
                )

        return data


class CommentDetailSerializer(serializers.ModelSerializer):

    issue = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "issue",
            "description",
            "date_created",
            "date_updated",
            "author",
        ]

    def get_issue(self, instance):
        queryset = instance.issue
        serializer = IssueListSerializer(queryset, many=False)
        return serializer.data


class CommentListSerializer(serializers.ModelSerializer):

    issue = serializers.SerializerMethodField

    class Meta:
        model = Comment
        fields = ["id", "issue", "description"]

    def get_issue(self, instance):
        queryset = instance.issue
        serializer = IssueListSerializer(queryset, many=False)
        return serializer.data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "birth_date", "age", "password"]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "birth_date",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "groups",
            "user_permissions",
        ]

    def validate_birth_date(self, birth_date):
        age = get_user_age(str(birth_date))
        if age < 15:
            raise serializers.ValidationError(
                "Vous n'avez pas" " l'age requis (15 ans)"
            )
        return birth_date


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "project", "user"]


class ContributorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "project", "user"]
