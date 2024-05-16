from SoftDeskApp.models import Project, Issue, Comment
from django import forms


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "type", "contributors"]


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            "project",
            "name",
            "description",
            "assigned_to",
            "priority",
            "nature",
            "status",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["issue", "description"]
