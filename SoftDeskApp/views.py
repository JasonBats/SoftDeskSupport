from django.shortcuts import render, redirect

from SoftDeskApp.models import Project, Issue, Comment
from SoftDeskSupport.settings import LOGIN_REDIRECT_URL
from SoftDeskApp.forms import ProjectForm, IssueForm, CommentForm


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
