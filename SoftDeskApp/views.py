from django.shortcuts import render, redirect

from SoftDeskApp.models import Project, Issue, Comment
from SoftDeskSupport.settings import LOGIN_REDIRECT_URL
from SoftDeskApp.forms import ProjectForm, IssueForm, CommentForm

from SoftDeskApp.serializers import (ProjectListSerializer,
                                     ProjectDetailSerializer,
                                     IssueListSerializer,
                                     IssueDetailSerializer,
                                     CommentListSerializer,
                                     CommentDetailSerializer
                                     )

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.contrib.auth.decorators import login_required
from SoftDeskApp.permissions import IsAdminAuthenticated


@login_required
def homepage(request):
    projects = Project.objects.all()
    issues = Issue.objects.all()
    comments = Comment.objects.all()
    user = request.user
    return render(
        request,
        'SoftDeskApp/home.html',
        context={
            'projects': projects,
            'user': user,
            'issues': issues,
            'comments': comments
        }
    )


def project_creation_view(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_instance = form.save(commit=False)
            project_instance.author = request.user
            project_instance.save()
            return redirect(LOGIN_REDIRECT_URL)
    return render(
        request,
        'SoftDeskApp/project_creation_form.html',
        context={'form': form})


def issue_creation_view(request):
    form = IssueForm
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue_instance = form.save(commit=False)
            issue_instance.author = request.user
            issue_instance.save()
            return redirect(LOGIN_REDIRECT_URL)
    return render(
        request,
        'SoftDeskApp/issue_creation_form.html',
        context={'form': form})

def comment_creation_view(request):
    form = CommentForm
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_instance = form.save(commit=False)
            comment_instance.author = request.user
            comment_instance.save()
            return redirect(LOGIN_REDIRECT_URL)
    return render(
        request,
        'SoftDeskApp/comment_creation.html',
        context={'form': form})

# vvv -- Viewsets de l'API ici -- vvv


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()


class IssueViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.all()


class AdminProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

# ^^^ -- Viewsets de l'API ici -- ^^^
