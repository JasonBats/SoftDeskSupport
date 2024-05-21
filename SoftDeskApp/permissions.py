from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission

from SoftDeskApp.models import Contributor, Issue


class IsProjectContributorAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.method == "POST":
            project_contributors = [
                user.user_id
                for user in Contributor.objects.filter(
                    project_id=request.data["project"]
                )
            ]
            if request.user.id in project_contributors:
                return True
            else:
                raise PermissionDenied(
                    "You must be contributing to this project to do this"
                )
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        project_contributors = [
            user.user_id for user in Contributor.objects.filter(project_id=obj.id)
        ]
        if isinstance(obj, Issue):
            project_contributors.extend(
                user.user_id
                for user in Contributor.objects.filter(project_id=obj.project)
            )

        return request.user.id in project_contributors


class IsRightUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return obj.author == request.user


class CanManageProjectContributors(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            contributing_to = [
                project.project_id
                for project in Contributor.objects.filter(user_id=request.user.id)
            ]

            if obj.project.id in contributing_to:
                return True
            else:
                raise PermissionDenied(
                    "You must be contributing to this project to do this"
                )
        elif request.method in SAFE_METHODS:
            return request.user.is_authenticated


class SignupViewPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
