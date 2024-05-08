from rest_framework import serializers
from SoftDeskApp.models import Project, Issue, Comment, Contributor
from authentication.models import User


class ProjectDetailSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_issues(self, instance):
        issues_queryset = Issue.objects.filter(project=instance)
        serializer = IssueListSerializer(issues_queryset, many=True)
        return serializer.data


class ProjectListSerializer(serializers.ModelSerializer):

    number_of_issues = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'author', 'number_of_issues']

    def get_number_of_issues(self, instance):
        number_of_issues_queryset = Issue.objects.filter(
            project=instance).count()
        return number_of_issues_queryset


class IssueDetailSerializer(serializers.ModelSerializer):

    project = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = '__all__'

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
        fields = ['id', 'name', 'description',
                  'author', 'assigned_to', 'project']


class CommentDetailSerializer(serializers.ModelSerializer):

    issue = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_issue(self, instance):
        queryset = instance.issue
        serializer = IssueListSerializer(queryset, many=False)
        return serializer.data


class CommentListSerializer(serializers.ModelSerializer):

    issue = serializers.SerializerMethodField

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'description']

    def get_issue(self, instance):
        queryset = instance.issue
        serializer = IssueListSerializer(queryset, many=False)
        return serializer.data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'birth_date', 'age', 'password']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError('Vous n\'avez pas'
                                              ' l\'age requis (15 ans)')


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'


class ContributorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'
